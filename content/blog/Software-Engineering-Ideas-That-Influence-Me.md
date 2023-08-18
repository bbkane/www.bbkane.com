+++
title = "Software Engineering Ideas That Influence Me"
date = 2019-08-11
updated = 2020-09-10
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

# Workflow

- [How I build a feature](https://simonwillison.net/2022/Jan/12/how-i-build-a-feature/) describes how Simon Wilson manages to maintain his dozens of projects with "**perfect commit**—one that bundles together the implementation, the tests, the documentation and a link to an external issue thread.". It's really inspired me to adopt much better (e2e/integration/snapshot) testing for my own projects to make them more maintainable.
- [Contributing to Complex Projects](https://mitchellh.com/writing/contributing-to-complex-projects) desribes somes useful steps to familiarize myself with giant projects. Super helpful; doing this can feel overwhelming.
- [My Approach to Building Large Technical Projects – Mitchell Hashimoto](https://mitchellh.com/writing/building-large-technical-projects) - "Demo-driven design". This post is super useful to motivate "what to work on next" for a project. If I'm not using this method, I can quickly go down multiple rabbit holes for a project and never have anything big to show for it (which I'm actually okay with for personal projects - the goal there is to have fun).
- [How do we get a tech team to make a big technical change? - Stack Overflow Blog](https://stackoverflow.blog/2023/05/10/how-do-we-get-a-tech-team-to-make-a-big-technical-change/) - how to make a technical change and bring the team along with you. This post explains so much about team "policitics" and I'm really trying to apply it to my work, especially after recently seeing projects get canceled/undone due to neglecting the team "context".
- [New talk: Learning DNS in 10 years](https://jvns.ca/blog/2023/05/08/new-talk-learning-dns-in-10-years/) describes how to learn difficult things over time. I'm currently trying to apply this method to learning about OpenID Connect.

# Architecture

- [Google's networked API Design Guide](https://cloud.google.com/apis/design/): Google's REST/RPC design guide is pretty opinionated, but looks very reasonable to me. I haven't designed many REST APIs, and I've been using this guide to shape how I design a side project of mine. In particular, creating "collection" and "item" abstractions and building operations on top of those has been revelatory (it turns out it's a common pattern, but I never noticed it before).
- [The Architecture of Open Source Applications](http://www.aosabook.org/en/index.html): a couple of free online books about the architecture of existing oplications. I've read parts of it, but I really need to read it in it's entirety.
- [GopherCon 2021: Arish Labroo - How we Go at Zillow - YouTube](https://www.youtube.com/watch?v=9Q1RMueVHAg) talks about productionalizing Go binaries to run HTTP services - timeouts, shutdowns, tracing, health checks, etc. Instead of going into the details about these aspects, Arish zooms out and focuses on how Zillow re-uses implementations with [google/wire: Compile-time Dependency Injection for Go](https://github.com/google/wire) to glue it all together. I really need to deepdive into this with some prototypes instead of only watching the talk.
- [Using Rust For Game Development](https://www.youtube.com/watch?v=aKLntZcp27M), [Is There More to Game Architecture than ECS?](https://www.youtube.com/watch?v=aKLntZcp27M), [SIMD at Insomniac Games: How We Do the Shuffle](https://www.gdcvault.com/play/1022248/SIMD-at-Insomniac-Games-How), and  [Parallelizing the Naughty Dog Engine Using Fibers](https://www.gdcvault.com/play/1022186/Parallelizing-the-Naughty-Dog-Engine) are examples of programming patterns that fall out of the somewhat extreme needs video game designs impose on their architects. I haven't tried these architectures but I really liked these talks.
- [Functional Core, Imperative Shell](https://www.destroyallsoftware.com/screencasts/catalog/functional-core-imperative-shell) and [Boundaries](https://www.destroyallsoftware.com/talks/boundaries): Gary Bernhart has a bunch of great videos on his [website](https://www.destroyallsoftware.com/screencasts). These two talks build off one another and talk about how you should make as much of your code as possible pure functions. This makes testing and extending it much easier.
- [Designing and Evaluating Reusable Components (2004)](https://caseymuratori.com/blog_0024): This talk is about what makes an API great. One particualr thing that stands out to me is how an API needs to cater to beginner users with simple functions yet also cater to more experienced users by offering more complicated knobs to twiddle.

# General Concepts / Ideas

- [The Grug Brained Developer](https://grugbrain.dev/) - This is an *excellent* list of somewhat disconnected advice about how to manage complexity in code, tests, and what works and what doesn't work, even though it looks nice on paper.
- [The Mathematical Hacker](https://www.evanmiller.org/mathematical-hacker.html): Evan Miller argues here that math is a tool for understanding the world, and that programmers should use it to do a lot of the heavy lifting. It's a bit of a reality check to some of my "well I can add this thingie here, and won't that be elegant" daydreams. Code is to solve a problem, and most of the harder problems are best solved mathmatically and simply transcribed as code.
- [Hammock Driven Development: Rich Hickey](https://www.youtube.com/watch?v=f84n5oFoZBc): Lectures like this are hard to come by. Rich Hickey gives wonderful tips on how to solve hard problems. The main one is that it can take a lot of time and conscious/unconscious thought to get an elegant solution.
- [CppCon 2014: Mike Acton "Data-Oriented Design and C++"](https://www.youtube.com/watch?v=rX0ItVEVjHc): This is another hugely influential talk. Mike Acton has a lot of efficiency-oriented ideas for designing code performantly.
- [Semantic Compression](https://caseymuratori.com/blog_0015): This post (and the rest of the series) have really helped me to grasp the "semantic compression" concept Casey uses here. I can actually trace its influence on my thought process through my historical code.


# Specific Concepts / Ideas

- [Safe and Efficient, Now](http://okmij.org/ftp/Computation/lightweight-static-guarantees.html): This site talks about how to use the type system to protect against invalid data. I particularly like the "DirtyString" example - using a separate type to represent untrusted data, along with a function that validates it and returns a validated version of the type. You can design your other functions to simply take an instance of the validated type, and be confident that they're already validated!
- [Against unnecessary databases](https://beepb00p.xyz/unnecessary-db.html) - This seems obvious in hindsight. However, I often get too eager to transform my data as I'm ingesting it and pay the price (difficult to understand, change, and test) later.
- [John Carmack: Best programming setup and IDE | Lex Fridman Podcast Clips - YouTube](https://www.youtube.com/watch?app=desktop&v=tzr7hRXcwkw) - In this interivew with Lex Friedman, John Carmack really makes a good case for getting really familiar with IDEs and debuggers instead of using text editors like Vim without language-aware tools. It has inspired me to be much more aggressive about learning the ins and outs of what VS Code (especially the debugger) can offer me. These days I have a hard time memorizing NeoVim's shortcuts and endlessly updating plugin ecosystem anyway. Also see [Why an IDE?](https://matklad.github.io/2020/11/11/yde.html).
- [What the heck is the event loop anyway? | Philip Roberts | JSConf EU - YouTube](https://www.youtube.com/watch?v=8aGhZQkoFbQ) is **THE BEST** explanation I've found on how async/await works. I need to refer back to it when I do anything somewhat complicated with async/await.
- [John Carmack on Inlined Code](http://number-none.com/blow/john_carmack_on_inlined_code.html): This John Carmack article talks about the benefits of inlining code that's only going to be called once. It also links to another functional programming article and you can follow that rabbit hole for far longer than you originally intended (don't ask me how I know that).
- [Advanced Testing in Go (Hashimoto)](https://www.youtube.com/watch?v=8hQG7QlcLBk) ([transcript](https://about.sourcegraph.com/go/advanced-testing-in-go)): In this talk, Michael Hashimoto splits his time between talking about creating tests creating testable code. Very useful and pragmatic.
- [How To Survive Your Project's First 100,000 Lines](https://verdagon.dev/blog/first-100k-lines) - a very nice checklist of specific tips on scaling a project.
- [Writing Python like Rust · Questions Nobody Asked..](https://oatzy.github.io/2020/05/10/writing-python-like-rust.html) - a short blog post to make Python code much easier to read about - type hints, structs, etc.
- [Make invalid states unrepresentable - GeekLaunch](https://geeklaunch.io/blog/make-invalid-states-unrepresentable/) - make code harder to misuse with Rust's type system.

- [Types as Sets](https://guide.elm-lang.org/appendix/types_as_sets.html): Types as Sets (unfortunately relegated to an appendix) really helped me understand how you can use types to force your data structures to be correct- to "make invalid states unrepresentable". Also see [this Handmade Hero QA](https://guide.handmadehero.org/code/day376/#8204) for a great overlapping explanation of discriminated unions in C/C++ and perhaps [What the Heck are Algebraic Data Types? ( for Programmers )](http://merrigrove.blogspot.com/2011/12/another-introduction-to-algebraic-data.html). If you're intrigued and want to really explore the math behind this, check out [The algebra (and calculus!) of algebraic data types](https://codewords.recurse.com/issues/three/algebra-and-calculus-of-algebraic-data-types) for an interesting exploration.
- [The Worst API Ever Made](https://caseymuratori.com/blog_0025): This is a rather hilarious post that really emphasizes how, when architecting a program, you should write the usage code first, so your users don't hate their experience with your API.


# Examples

These are libraries that have really impressed me with their usability;
whatever they're doing, I want to emulate it!

- Python's [pathlib](https://docs.python.org/3/library/pathlib.html) library - `pathlib` is easily my preferred way to work with paths. Most (all?) methods returns a new instance instead of mutating.
- Python's [requests](https://3.python-requests.org/) library - `requests` optimizes for the common case (making a single HTTP request), but provides mechanisms for TCP connection reuse, auto-adding headers, authorization, and many other conveniences for dealing with HTTP. [encode/httpx: A next generation HTTP client for Python. 🦋](https://github.com/encode/httpx/) is an async/await library that's very similar and maturing nicely. Hopefully one day it'll [reach 1.0](https://github.com/encode/httpx/issues/947).
- [SQLite3](https://www.sqlite.org/index.html) - SQLite3 runs everywhere, has insanely good docs, and is so useful it might be [the most used library in the world](https://www.sqlite.org/mostdeployed.html).
- Go's [kingpin](https://github.com/alecthomas/kingpin) library - `kingpin` provides a relatively simple way to parse command line arguments for Go programs. It exposes a powerful yet readable fluent-style API that makes it fairly easy to do what you want to do.
- [python-trio/trio: Trio – a friendly Python library for async concurrency and I/O](https://github.com/python-trio/trio) is a really innovative async/await framework for Python. Most of the innovations are described in [Notes on structured concurrency, or: Go statement considered harmful — njs blog](https://vorpus.org/blog/notes-on-structured-concurrency-or-go-statement-considered-harmful/).
- [tiangolo/fastapi: FastAPI framework, high performance, easy to learn, fast to code, ready for production](https://github.com/tiangolo/fastapi) is one of the newer Python libraries that are "IDE ready" - very well type-hinted to make it easy for IDEs to inspect and offer auto-completion for.
- [WTF Dial](https://wtfdial.com/) Ben B Johnson wrote this app and an (incomplete) series of blog posts about how it works. I really like it because there's very little library usage. He's implementing things "by hand". I've learned a lot by reading the blog posts and studying the source code.
