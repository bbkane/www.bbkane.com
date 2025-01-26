+++
title = "Storing a Go Slice in a MySQL Column"
date = 2025-01-25
+++

I recently had to write code to store a `[]string` in a MySQL `JSON` column. Because the MySQL driver interface speaks bytes, this can be easily done by marshaling the JSON into `[]byte` before sending it to the databse and unmarshaling the JSON into the `[]string` after retrieving it from the database. I looked into ways to make this code more convenient, since that's a decent amount of work for each query. 

Finally, I cobbled together the right interfaces. Now, I can run:

```go
// insert
stringSlice := []string{"first", "second"}
query := "INSERT INTO table_name (string_slice) VALUES (?))"
param := Array(&stringSlice)
_, err := d.db.Exec(query, param)
```

```go
// select
query := "SELECT string_slice FROM table_name WHERE table_name_id = 1"
var stringSlice []string
err := d.db.QueryRow(query).Scan(Array(&stringSlice))
```

This is accomplished in two parts.

First, implement the[`driver.Valuer`](https://pkg.go.dev/database/sql/driver#Valuer) and [`sql.Scanner`](https://pkg.go.dev/database/sql#Scanner) interfaces with a `StringArray` type. This part is informed by [StackOverflow](https://stackoverflow.com/questions/72851745/how-can-i-access-json-column-in-mysql-db-from-golang).

```go
// StringArray is a custom type that implements the sql.Scanner and driver.Valuer interfaces
type StringArray []string

var _ driver.Valuer = StringArray{}
var _ sql.Scanner = &StringArray{}

// Value implements the driver.Valuer interface
func (a StringArray) Value() (driver.Value, error) {
	return json.Marshal(a)
}

// Scan implements the sql.Scanner interface
func (a *StringArray) Scan(value interface{}) error {
	if value == nil {
		*a = nil
		return nil
	}

	bytes, ok := value.([]byte)
	if !ok {
		return fmt.Errorf("expected bytes: %v", value)
	}

	return json.Unmarshal(bytes, a)
}
```

Second, add a wrapper function (`Array`) to avoid runtime errors when calling `Scan`. This part is heavily inspired by [`lib/pq`'s `Array` function'](https://github.com/lib/pq/blob/b7ffbd3b47da4290a4af2ccd253c74c2c22bfabf/array.go#L29), and to be honest I don't completely understand why it's needed. If you don't do it, the `sql` library complains at runtime when you try to `SELECT`. I only need to work with slices of strings, but this is easily extended by adding more `XxxArray`s .

```go
func Array(a interface{}) interface {
	driver.Valuer
	sql.Scanner
} {
	switch a := a.(type) {
	case []string:
		return (*StringArray)(&a)
	case *[]string:
		return (*StringArray)(a)
	default:
		panic(fmt.Sprintf("unsupported type: %T", a))
	}
}
```

