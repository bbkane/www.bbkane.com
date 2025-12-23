+++
title = "Sending OTEL metrics to OpenObserve"
date = 2025-06-01
+++

The usual flow for OTEL metrics (as well as traces, and probably logs) is:

```
App -> OTEL Collector -> Observability Platform
```



<!--

```mermaid
sequenceDiagram
    participant App
    participant OTELCollector as OTEL Collector
    participant ObservabilityPlatform as Observability Platform

    App ->> OTELCollector: Send telemetry data over localhost
    OTELCollector ->> ObservabilityPlatform: Forward processed data
```

-->

This works fantastically for large deployments, but for smaller deployments or dev work, it's a pain to set up. Fortunately, we can install a local instance of [OpenObserve](https://openobserve.ai/) to act as both the [OTEL Collector](https://opentelemetry.io/docs/collector/) as well as the Observability Platform. This provides an easy, private way to experiment with OTEL observability, without paying most of the setup costs.

```
App -> OpenObserve
```



<!--

```mermaid
sequenceDiagram
    participant App
    participant OpenObserve

    App ->> OpenObserve: Send telemetry data over localhost

```

-->

I really enjoy OpenObserve because the devs intentionally focus on setup ease.

# Install and Run OpenObserve

After [downloading OpenObserve](https://github.com/openobserve/openobserve/releases/), start it with command similar to the following (or see [the docs](https://openobserve.ai/docs/environment-variables/) if you want to configure it more):

```bash
ZO_ROOT_USER_EMAIL=root@example.com \
ZO_ROOT_USER_PASSWORD=pass \
./openobserve
```

Then head to [http://localhost:5080/web/ingestion/recommended/traces?org_identifier=default](http://localhost:5080/web/ingestion/recommended/traces?org_identifier=default) and note configuration we'll use to connect:

> **OTLP HTTP**
>
> ```
> HTTP Endpoint: http://localhost:5080/api/default
> Authorization: Basic cm9vdEBleGFtcGxlLmNvbTpabFhiTXZTMENYSEtubzJ4
> ```

(NOTE: the authorization header base64 string appears to have changed between OpenObserve 0.14.x and 0.15.x, even with the same password). So make sure to copy it from the link.

# Emit metrics from our code

Here's some sample Go code to emit metrics:
<details>

```go
package main

import (
	"context"
	"fmt"
	"math/rand"
	"os"
	"os/signal"
	"time"

	"go.opentelemetry.io/otel"
	"go.opentelemetry.io/otel/attribute"
	"go.opentelemetry.io/otel/exporters/otlp/otlpmetric/otlpmetrichttp"
	"go.opentelemetry.io/otel/metric"
	sdkmetric "go.opentelemetry.io/otel/sdk/metric"
)

// adapted from https://opentelemetry.io/docs/languages/go/instrumentation/#metrics

const name = "otel_metrics"

var (
	meter       = otel.Meter(name)
	rollCnt     metric.Int64Counter
	durationCnt metric.Float64ObservableCounter
)

func init() {
	rollCnt = must(meter.Int64Counter(
		"dice.rolls",
		metric.WithDescription("The number of rolls by roll value"),
		metric.WithUnit("{roll}"),
	))
	durationCnt = must(meter.Float64ObservableCounter(
		"uptime",
		metric.WithDescription("The duration since the application started."),
		metric.WithUnit("s"),
	))
}

func must[T any](v T, err error) T {
	if err != nil {
		panic(err)
	}
	return v
}

func main() {
	start := time.Now()

	ctx, cancel := signal.NotifyContext(context.Background(), os.Interrupt)
	defer func() {
		fmt.Println("calling cancel")
		cancel()
	}()

	// can also use a stdout exporter
	// metricsExporter := must(stdoutmetric.New(stdoutmetric.WithPrettyPrint()))
	metricsExporter := must(otlpmetrichttp.New(context.Background()))
	meterProvider := sdkmetric.NewMeterProvider(
		sdkmetric.WithReader(
			sdkmetric.NewPeriodicReader(
				metricsExporter,
				sdkmetric.WithInterval(5*time.Second),
			),
		),
	)
	defer func() {
		fmt.Println("calling meterProvider shutdown")
		_ = meterProvider.Shutdown(context.Background())
	}()
	otel.SetMeterProvider(meterProvider)

	// Register the observable counter
	// This callback is called every time the metrics provider exports (in our case every 5 seconds)
	reg := must(meter.RegisterCallback(
		func(_ context.Context, observer metric.Observer) error {
			observer.ObserveFloat64(
				durationCnt,
				time.Since(start).Seconds(),
				metric.WithAttributes(
					attribute.String("key", "value"),
				),
			)
			return nil
		},
		durationCnt,
	))

	defer func() {
		fmt.Println("calling meter unregister")
		reg.Unregister()
	}()

	ticker := time.NewTicker(1 * time.Second)
	defer func() {
		fmt.Println("calling ticker stop")
		ticker.Stop()
	}()
	for {
		select {
		case <-ctx.Done():
			fmt.Println("context done")
			return
		case <-ticker.C:
			fmt.Println("rolling dice")
			roll := 1 + rand.Intn(6)
			// use the synchronous counter
			rollCnt.Add(ctx, 1, metric.WithAttributes(
				attribute.Int("roll.value", roll),
			))
		}
	}
}
```

</details>

The most important bit here is the `exporter` set up:

```go
metricsExporter := must(otlpmetrichttp.New(context.Background()))
```

This tells our code to export our metrics over HTTP. We'll use env vars to tell the collector where to send these metrics.

# Run our code with OTEL env vars set

Next, we need to run our app with the appropriate [exporter  `OTEL_*` env vars](https://opentelemetry.io/docs/languages/sdk-configuration/otlp-exporter/) set so it can connect to our local OpenObserve instance:

```bash
OTEL_EXPORTER_OTLP_ENDPOINT='http://127.0.0.1:5080/api/default' \
OTEL_EXPORTER_OTLP_HEADERS='Authorization=Basic cm9vdEBleGFtcGxlLmNvbTpabFhiTXZTMENYSEtubzJ4' \
go run .
```

# View Metrics from OpenObserve

Head to the metrics tab, and run a query. I like to use "Auto" and click the values in the sidebar to form my graph:

![image-20250601070439889](index.assets/image-20250601070439889.png)

In this screenshot, I:

- selected the `dice_rolls` stream
- changed the query method to "Audo"
- Clicked `+X` for `start_time`
- Clicked `+B` for `roll_value`
- Clicked `+Y` for `value`
- Clicked "Run Query"

As expected, we can see that our dice is fair - in that timespan and several rolls, each number continues to show an equal probability of being rolled.

# Next Steps

Of course, this is the bare minimum to get started with OTEL and OpenObserve. Further ideas:

- Skip the local install step and send metrics to [OpenObserve Cloud](https://openobserve.ai/docs/quickstart/)
- Install OpenObserve on a server you control (I do this with [Ansible](https://github.com/bbkane/shovel_ansible/blob/master/openobserve.ansible.yaml))
- Create an org instead of using the default one like this post does
- Send traces / logs to OpenObserve as well!
- Make a dashboard with these metrics

# Bonus: testing metrics in memory

This isn't super related to exporting metrics, but it's also not too difficult to set up an exporter that saves metrics in-memory for testing purposes. The hardest part is gluing together the APIs (thanks ChatGPT):

<details>

```go
package otel_inmem_test

import (
	"context"
	"testing"

	"github.com/stretchr/testify/require"
	"go.opentelemetry.io/otel/sdk/metric"
	"go.opentelemetry.io/otel/sdk/metric/metricdata"
)

func TestMyMetrics(t *testing.T) {
	require := require.New(t)
	ctx := context.Background()
	reader := metric.NewManualReader()

	provider := metric.NewMeterProvider(metric.WithReader(reader))

	// everything is in scope in this test, so no need to set global meter provider. But if needed:
	// otel.SetMeterProvider(provider)

	meter := provider.Meter("test")
	counter, err := meter.Int64Counter("my_counter")
	require.NoError(err)

	counter.Add(ctx, 5)
	counter.Add(ctx, 10)

	// Collect the metrics
	var rm metricdata.ResourceMetrics
	err = reader.Collect(ctx, &rm)
	require.NoError(err)

	require.Equal(1, len(rm.ScopeMetrics))
	require.Equal(1, len(rm.ScopeMetrics[0].Metrics))

	err = provider.Shutdown(ctx)
	require.NoError(err)
}
```

</details>
