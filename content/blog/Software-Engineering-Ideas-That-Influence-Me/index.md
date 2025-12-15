+++
title = "Software Engineering Ideas That Influence Me"
date = 2019-08-11
updated = 2025-09-19
aliases = [ "2019/08/11/Software-Engineering-Ideas-That-Influence-Me.html" ]

+++

I watch a lot of conference talks on YouTube and I read a lot of software
engineering articles. Some of that media has really helped me become a better
engineer. As a relative newcomer to engineering, I know my style will develop further and
my current judgment of "best practice" will change (and I can see how it's
changed historically by looking at my old code), but I plan to read/watch these
resources every year. I look forward to future me gaining new perspective on
them.

I've tried to categorize these links, but naturally there's some overlap :)

In some cases, I'll remove links if I feel like I can expand the concept into a separate blog post and link from that.

# Workflow

- [How I build a feature](https://simonwillison.net/2022/Jan/12/how-i-build-a-feature/) describes how Simon Wilson manages to maintain his dozens of projects with "**perfect commit**—one that bundles together the implementation, the tests, the documentation and a link to an external issue thread.". It's really inspired me to adopt much better (e2e/integration/snapshot) testing for my own projects to make them more maintainable.
- [Contributing to Complex Projects](https://mitchellh.com/writing/contributing-to-complex-projects) desribes somes useful steps to familiarize myself with giant projects. Super helpful; doing this can feel overwhelming.
- [My Approach to Building Large Technical Projects – Mitchell Hashimoto](https://mitchellh.com/writing/building-large-technical-projects) - "Demo-driven design". This post is super useful to motivate "what to work on next" for a project. If I'm not using this method, I can quickly go down multiple rabbit holes for a project and never have anything big to show for it (which I'm actually okay with for personal projects - the goal there is to have fun).
- [New talk: Learning DNS in 10 years](https://jvns.ca/blog/2023/05/08/new-talk-learning-dns-in-10-years/) describes how to learn difficult things over time. Also see [New talk: Making Hard Things Easy](https://jvns.ca/blog/2023/10/06/new-talk--making-hard-things-easy/)
- [Getting things done (in small increments)](https://dubroy.com/blog/getting-things-done-in-small-increments/) has really practical advice when you don't have a lot of time (he's a parent too!)

# Culture

- [Why I Ignore The Spotlight as a Staff Engineer](https://lalitm.com/software-engineering-outside-the-spotlight/) and [Software engineering under the spotlight](https://www.seangoedecke.com/the-spotlight/) are two really good posts succeeding in different types of engineering culture.
- [How do we get a tech team to make a big technical change? - Stack Overflow Blog](https://stackoverflow.blog/2023/05/10/how-do-we-get-a-tech-team-to-make-a-big-technical-change/) - how to make a technical change and bring the team along with you. This post explains so much about team "policitics" and I'm really trying to apply it to my work, especially after recently seeing projects get canceled/undone due to neglecting the team "context".

# General Concepts / Ideas

- [The Grug Brained Developer](https://grugbrain.dev/) - This is an *excellent* list of somewhat disconnected advice about how to manage complexity in code, tests, and what works and what doesn't work, even though it looks nice on paper.
- [The Mathematical Hacker](https://www.evanmiller.org/mathematical-hacker.html): Evan Miller argues here that math is a tool for understanding the world, and that programmers should use it to do a lot of the heavy lifting. It's a bit of a reality check to some of my "well I can add this thingie here, and won't that be elegant" daydreams. Code is to solve a problem, and most of the harder problems are best solved mathmatically and simply transcribed as code.
- [Hammock Driven Development: Rich Hickey](https://www.youtube.com/watch?v=f84n5oFoZBc): Lectures like this are hard to come by. Rich Hickey gives wonderful tips on how to solve hard problems. The main one is that it can take a lot of time and conscious/unconscious thought to get an elegant solution.
- [Semantic Compression](https://caseymuratori.com/blog_0015): This post (and the rest of the series) have really helped me to grasp the "semantic compression" concept Casey uses here. I can actually trace its influence on my thought process through my historical code.

# Architecture

- [Google's networked API Design Guide](https://cloud.google.com/apis/design/): Google's REST/RPC design guide is pretty opinionated, but looks very reasonable to me. I haven't designed many REST APIs, and I've been using this guide to shape how I design a side project of mine. In particular, creating "collection" and "item" abstractions and building operations on top of those has been revelatory (it turns out it's a common pattern, but I never noticed it before).
- [The Architecture of Open Source Applications](http://www.aosabook.org/en/index.html): a couple of free online books about the architecture of existing applications. I've read parts of it, but I really need to read it in it's entirety.
- [GopherCon 2021: Arish Labroo - How we Go at Zillow - YouTube](https://www.youtube.com/watch?v=9Q1RMueVHAg) talks about productionalizing Go binaries to run HTTP services - timeouts, shutdowns, tracing, health checks, etc. Instead of going into the details about these aspects, Arish zooms out and focuses on how Zillow re-uses implementations with [google/wire: Compile-time Dependency Injection for Go](https://github.com/google/wire) to glue it all together. I really need to deepdive into this with some prototypes instead of only watching the talk.
- [Functional Core, Imperative Shell](https://www.destroyallsoftware.com/screencasts/catalog/functional-core-imperative-shell) and [Boundaries](https://www.destroyallsoftware.com/talks/boundaries): Gary Bernhart has a bunch of great videos on his [website](https://www.destroyallsoftware.com/screencasts). These two talks build off one another and talk about how you should make as much of your code as possible pure functions. This makes testing and extending it much easier.
- [Designing and Evaluating Reusable Components (2004)](https://caseymuratori.com/blog_0024): This talk is about what makes an API great. One particular thing that stands out to me is how an API needs to cater to beginner users with simple functions yet also cater to more experienced users by offering more complicated knobs to twiddle. Also see [API Design by Carson Gross ~ BSDC 2025 - YouTube](https://www.youtube.com/watch?v=dTstnhS3moc).
- [Making Impossible States Impossible: Type-Safe Domain Modeling with Functional Dependency Injection · cekrem.github.io](https://cekrem.github.io/posts/making-impossible-states-impossible-with-functional-dependency-injection/) - this is nice because it shows how Elm's type system can be used to layer an API.
- [Linux kernel design patterns - part 3 [LWN.net]](https://lwn.net/Articles/336262/) - really good article about "mid layers" that should probably be libraries.
- [Crash-only software: More than meets the eye [LWN.net]](https://lwn.net/Articles/191059/) - designing software to be able to recover from crashes
- [The server chose violence - Cliffle](https://cliffle.com/blog/hubris-reply-fault/#the-server-isn-t-having-any-of-your-nonsense-either) talks about how software designed to "fail fast" facilitates more correctness. Also see [Zig And Rust](https://matklad.github.io/2023/03/26/zig-and-rust.html), a really great comparison of two styles to provide reliable software.
- [Rails World 2024 Opening Keynote - David Heinemeier Hansson - YouTube](https://www.youtube.com/watch?v=-cEn_83zRFw) - talks about the "one person framework". In addition to describing the architecture, it's just a really fun talk to listen to in general.
- Web app architecture: [Everything I know about good API design](https://www.seangoedecke.com/good-api-design/) , [PAGNIs: Probably Are Gonna Need Its](https://simonwillison.net/2021/Jul/1/pagnis/), [YAGNI exceptions - lukeplant.me.uk](https://lukeplant.me.uk/blog/posts/yagni-exceptions/)
- Architecture talks I found super interesting, even though I doubt I'll need to build similar ones.
  - [Using Rust For Game Development](https://www.youtube.com/watch?v=aKLntZcp27M)
  - [Is There More to Game Architecture than ECS?](https://www.youtube.com/watch?v=aKLntZcp27M)
  - [SIMD at Insomniac Games: How We Do the Shuffle](https://www.gdcvault.com/play/1022248/SIMD-at-Insomniac-Games-How)
  - [Parallelizing the Naughty Dog Engine Using Fibers](https://www.gdcvault.com/play/1022186/Parallelizing-the-Naughty-Dog-Engine)
  - [Neovim & Extensibility - My Talk from Jane Street - YouTube](https://www.youtube.com/watch?v=MQBr9hwf0BY)


# Data oriented design

I don't actually write a lot of explicitly data oriented designed programs (most of my code is probably best categorized as "automation" or "web software", which don't require this level of performance) but man there are some great talks about it!! Data-oriented design originated in game programming, but some compiler teams have taken hold of it.

- [CppCon 2014: Mike Acton "Data-Oriented Design and C++"](https://www.youtube.com/watch?v=rX0ItVEVjHc): This is another hugely influential talk. Mike Acton has a lot of efficiency-oriented ideas for designing code performantly.
- [Andrew Kelley - Practical DOD on Vimeo](https://vimeo.com/649009599) - this is something of a successor talk to Acton's talk.
- [Programming without pointers](https://www.hytradboi.com/2025/05c72e39-c07e-41bc-ac40-85e8308f2917-programming-without-pointers) - Andrew Kelly explains how programming without pointers can be super performant
- [Data-Oriented Design Revisited: Type Safety in the Zig Compiler - Matthew Lugg - YouTube](https://www.youtube.com/watch?v=KOZcJwGdQok) - a more concrete talk about how the Zig compiler team continued the data oriented deisgn
- [Modernizing Compiler Design for Carbon Toolchain - Chandler Carruth - CppNow 2023 - YouTube](https://www.youtube.com/watch?v=ZI198eFghJk) - another good talk about the Carbon language compiler design.

# Using Types for Correctness

There's a lot of repetitiveness here, but I think seeing concepts explained in different ways with different examples can be very helpful.

- [Writing Python like Rust · Questions Nobody Asked..](https://oatzy.github.io/2020/05/10/writing-python-like-rust.html) - a short blog post to make Python code much easier to read about - type hints, structs, etc. Also see [Writing Python like it’s Rust | Kobzol’s blog](https://kobzol.github.io/rust/python/2023/05/20/writing-python-like-its-rust.html) for similar/more tips.
- [Make invalid states unrepresentable - GeekLaunch](https://geeklaunch.io/blog/make-invalid-states-unrepresentable/) - make code harder to misuse with Rust's type system. [Making Illegal States Unrepresentable—In TypeScript — Sympolymathesy, by Chris Krycho](https://v5.chriskrycho.com/journal/making-illegal-states-unrepresentable-in-ts/) is a similar talk using TypeScript. [The Typestate Pattern in Rust - Cliffle](https://cliffle.com/blog/rust-typestate/) is another really good explaination of this.
- [Types as Sets](https://guide.elm-lang.org/appendix/types_as_sets.html): Types as Sets (unfortunately relegated to an appendix) really helped me understand how you can use types to force your data structures to be correct- to "make invalid states unrepresentable". Also see [this Handmade Hero QA](https://guide.handmadehero.org/code/day376/#8204) for a great overlapping explanation of discriminated unions in C/C++ and perhaps [What the Heck are Algebraic Data Types? ( for Programmers )](http://merrigrove.blogspot.com/2011/12/another-introduction-to-algebraic-data.html). If you're intrigued and want to really explore the math behind this, check out [The algebra (and calculus!) of algebraic data types](https://codewords.recurse.com/issues/three/algebra-and-calculus-of-algebraic-data-types) for an interesting exploration.
- [Safe and Efficient, Now](http://okmij.org/ftp/Computation/lightweight-static-guarantees.html): This site talks about how to use the type system to protect against invalid data. I particularly like the "DirtyString" example - using a separate type to represent untrusted data, along with a function that validates it and returns a validated version of the type. You can design your other functions to simply take an instance of the validated type, and be confident that they're already validated!
- [Haskell mini-patterns handbook :: Kowainik](https://kowainik.github.io/posts/haskell-mini-patterns) - goes over several patterns - newtype, evidence, etc. I think some of these are more complicated than valuable (i.e., does it really matter how will it works if the compile errors if you mis-hold it are terrible, and you can't explain it to the new guy?), but I also appreciate the quick summaries and examples.
- [Abuse of Sum Types In OO Languages - iRi](https://www.jerf.org/iri/post/2960/) talks about how to get some of the advantages of Sum types, even if your language doesn't support them.

# How to Debug

This is a mix of debugging advice as well as "war stories" for examples

- [A systematic approach to debugging | nicole@web](https://ntietz.com/blog/how-i-debug-2023/) - a super nice checklist to systematically debug instead of randomly trying things
- [stas00/the-art-of-debugging: The Art of Debugging](https://github.com/stas00/the-art-of-debugging?tab=readme-ov-file) - has a lot more detailed things to try when debugging
- [Linux Performance Analysis in 60,000 Milliseconds | by Netflix Technology Blog | Netflix TechBlog](https://netflixtechblog.com/linux-performance-analysis-in-60-000-milliseconds-accc10403c55) - good Linux commands to try when things start slowing down. Also see [Brendan Gregg's Homepage](https://www.brendangregg.com/)
- [David A. Wheeler's Review of "Debugging" by David J. Agans](https://dwheeler.com/essays/debugging-agans.html) - another debugging checklist (and see [comments](https://news.ycombinator.com/item?id=42682602) too)

# Observability

This is mostly focused on OpenTelemetry, since I really like the "protocol over specific vendors" approach they provide:

- [An Observable Service with No Logs - InfoQ](https://www.infoq.com/presentations/event-tracing-monitoring/) - a company replaced logs with tracing and reported how it went. I'm trying to do the same thing for side projects, so I find this super interesting.
- [Tracing: structured logging, but better in every way | Andy Dote](https://andydote.co.uk/2023/09/19/tracing-is-better/) and [HN comments](https://news.ycombinator.com/item?id=37562593) - Andy Cote gives a great overview of replacing tracing with logs, including screenshots and code samples.
- [Building dashboards for operational visibility | Amazon Builders' Library](https://aws.amazon.com/builders-library/building-dashboards-for-operational-visibility/) - very specific advice for building good dashboards.
- [Grafana dashboards | Grafana Labs](https://grafana.com/grafana/dashboards/) - a library of dashboards voted on by the Grafana community! Great for inspiration! Also see their docs for each [visualization](https://grafana.com/docs/grafana/latest/visualizations/panels-visualizations/visualizations/).
- [Observability as code (Grafana)](https://grafana.com/blog/2025/05/07/observability-as-code-grafana-12/) - This is more inspirational, but shows some exciting ways to model dashboards as code.

# Testing / Formal methods

- [Advanced Testing in Go (Hashimoto)](https://www.youtube.com/watch?v=8hQG7QlcLBk) ([transcript](https://about.sourcegraph.com/go/advanced-testing-in-go)): In this talk, Michael Hashimoto splits his time between talking about creating tests creating testable code. Very useful and pragmatic.
- ["Testing Distributed Systems w/ Deterministic Simulation" by Will Wilson - YouTube](https://www.youtube.com/watch?app=desktop&v=4fFDFbi3toc) - this is the original deterministic simulation testing talk - this approach has since been copied by several projects and Will Wilson (the speaker) has launched [a company](https://antithesis.com/) to offer DST as a service
- [What Isn't Your System Supposed to Do? by Hillel Wayne - YouTube](https://www.youtube.com/watch?v=d9cM8f_qSLQ) - a SUPER good introduction into how to think about distributed systems and where they can go wrong.
- [Reliable software: An interview with Jon Gjengset - timClicks (Tim McNamara)](https://timclicks.dev/podcast/reliable-software-an-interview-with-jon-gjengset) - extremely interesting talk about the 'spectrum' of testing software (with a focus on Rust). I've listened to this a few times and I think I'm actually due for another listen
- [Systems Correctness Practices at Amazon Web Services – Communications of the ACM](https://cacm.acm.org/practice/systems-correctness-practices-at-amazon-web-services/) - article about how AWS ensures their distributed systems are correct. Covers some of the same things as previous links but also some specific problems they've faced (education, metastability).
- [Turso simulator README](https://github.com/tursodatabase/turso/tree/main/simulator) - an implementation of DST for a SQL database. It has a good explanation of the different parts involved.
- [Demystifying monads in Rust through property-based testing · sunshowers](https://sunshowers.io/posts/monads-through-pbt/) - super good intro into property testing and how to make it inefficient with monads. I particularly like the explanation of growing and shrinking inputs and how to compose those.

# Platforms

- [komoroske.com/gardening-platforms - Google Slides](https://docs.google.com/presentation/d/1cY95dRixFho0pMIlrEFcGL_XKVy9vnE4NGOD6TQMj50/edit?slide=id.p#slide=id.p) - This talks about how building, evolving, and growing platforms
- [Stevey's Google Platforms Rant](https://gist.github.com/chitchcock/1281611) - This (unintentionally made public) rant about how Google can't make platforms is hilarious and has a lot of insight about how Amazon succeeded as a platform while Google hadn't (and even today it's not nearly as successful)
- [Platform as a Reflection of Values - YouTube](https://www.youtube.com/watch?v=Xhx970_JKX4) - Bryan Cantrill reflects on why NodeJS was the wrong choice for his company, and also how a platform must make fundamental tradeoffs supporting an audience
- [Dear Google Cloud: Your Deprecation Policy is Killing You | by Steve Yegge | Medium](https://steve-yegge.medium.com/dear-google-cloud-your-deprecation-policy-is-killing-you-ee7525dc05dc) - Steve Yegge talks once again about how platforms must remain stable for customers to trust them.

# Specific Concepts / Ideas

- [Against unnecessary databases](https://beepb00p.xyz/unnecessary-db.html) - This seems obvious in hindsight. However, I often get too eager to transform my data as I'm ingesting it and pay the price (difficult to understand, change, and test) later.
- [John Carmack: Best programming setup and IDE | Lex Fridman Podcast Clips - YouTube](https://www.youtube.com/watch?app=desktop&v=tzr7hRXcwkw) - In this interivew with Lex Friedman, John Carmack really makes a good case for getting really familiar with IDEs and debuggers instead of using text editors like Vim without language-aware tools. It has inspired me to be much more aggressive about learning the ins and outs of what VS Code (especially the debugger) can offer me. These days I have a hard time memorizing NeoVim's shortcuts and endlessly updating plugin ecosystem anyway. Also see [Why an IDE?](https://matklad.github.io/2020/11/11/yde.html).
- [What the heck is the event loop anyway? | Philip Roberts | JSConf EU - YouTube](https://www.youtube.com/watch?v=8aGhZQkoFbQ) is **THE BEST** explanation I've found on how async/await works. I need to refer back to it when I do anything somewhat complicated with async/await.
- [John Carmack on Inlined Code](http://number-none.com/blow/john_carmack_on_inlined_code.html): This John Carmack article talks about the benefits of inlining code that's only going to be called once. It also links to another functional programming article and you can follow that rabbit hole for far longer than you originally intended (don't ask me how I know that).
- [How To Survive Your Project's First 100,000 Lines](https://verdagon.dev/blog/first-100k-lines) - a very nice checklist of specific tips on scaling a project.
- [The Worst API Ever Made](https://caseymuratori.com/blog_0025): This is a rather hilarious post that really emphasizes how, when architecting a program, you should write the usage code first, so your users don't hate their experience with your API.
- [HTML First](https://html-first.com/) - this site explains how to build frontends with HTML first, instead of large JavaScript dependencies. I want to do this primarily because I think it's more maintainable.
- [Write code that is easy to delete, not easy to extend](https://programmingisterrible.com/post/139222674273/write-code-that-is-easy-to-delete-not-easy-to)  - really good article about how locking into an architecture too early can hurt you, and when it's worth it.

# Example Code

These are libraries that have really impressed me with their usability;
whatever they're doing, I want to emulate it!

- Python's [pathlib](https://docs.python.org/3/library/pathlib.html) library - `pathlib` is easily my preferred way to work with paths. Most (all?) methods returns a new instance instead of mutating.
- Python's [requests](https://3.python-requests.org/) library - `requests` optimizes for the common case (making a single HTTP request), but provides mechanisms for TCP connection reuse, auto-adding headers, authorization, and many other conveniences for dealing with HTTP. [encode/httpx: A next generation HTTP client for Python. 🦋](https://github.com/encode/httpx/) is an async/await library that's very similar and maturing nicely. Hopefully one day it'll [reach 1.0](https://github.com/encode/httpx/issues/947).
- [earthboundkid/requests](https://github.com/earthboundkid/requests) is a Go library to make HTTP requests that follows a super nice builder pattern compared to the stdlib. See the README for side by side examples.
- [SQLite3](https://www.sqlite.org/index.html) - SQLite3 runs everywhere, has insanely good docs, and is so useful it might be [the most used library in the world](https://www.sqlite.org/mostdeployed.html).
- Go's [kingpin](https://github.com/alecthomas/kingpin) library - `kingpin` provides a relatively simple way to parse command line arguments for Go programs. It exposes a powerful yet readable fluent-style API that makes it fairly easy to do what you want to do.
- [python-trio/trio: Trio – a friendly Python library for async concurrency and I/O](https://github.com/python-trio/trio) is a really innovative async/await framework for Python. Most of the innovations are described in [Notes on structured concurrency, or: Go statement considered harmful — njs blog](https://vorpus.org/blog/notes-on-structured-concurrency-or-go-statement-considered-harmful/).
- [tiangolo/fastapi: FastAPI framework, high performance, easy to learn, fast to code, ready for production](https://github.com/tiangolo/fastapi) is one of the newer Python libraries that are "IDE ready" - very well type-hinted to make it easy for IDEs to inspect and offer auto-completion for.
- [WTF Dial](https://wtfdial.com/) Ben B Johnson wrote this app and an (incomplete) series of blog posts about how it works. I really like it because there's very little library usage. He's implementing things "by hand". I've learned a lot by reading the blog posts and studying the source code.

# Example Stories

- [Hachyderm: Decentralized Social Media - YouTube](https://www.youtube.com/watch?app=desktop&v=5KU10K3EXK4) talks about Kris Nóva's experience scaling Hachyderm.
- [Sometimes it *is* a compiler bug](https://quick-lint-js.com/blog/bug-journey/) - a bug in the compiler!!
