+++
title = "Checklists And Sayings"
date = 2019-08-25
updated = 2020-12-17
aliases = [ "2019/08/25/Useful-Checklists.html", "blog/useful-checklists" ]
+++

These are fairly small lists that I want to read every once in a while.

## Releasing Software for Humans

- Design from the user perspective
- Don't advertise until close to finishing
- Timing is important. Don't announce something cool when there's something else going on
- Include usage example in README.md
- Test on all platforms users use
- Include call for feedback in `--help`, and solicit users to use it
- You only get one first impression
- Separate user docs from developer docs
- Manually run through the full setup and some common scenarios before you demo.

## What To Put in Function Documentation

I love this [section](https://cloud.google.com/apis/design/documentation#checklist) of Google's API design book.

### Checklist for all descriptions

Make sure each description is brief but complete and can be understood by users
who don't have additional information about the API. In most cases, there's
more to say than just restating the obvious; for example, the description of
the `series.insert` method shouldn't just say "Inserts a series." — while your
naming should be informative, most readers are reading your descriptions
because they want more information than the names themselves provide. If you're
not sure what else to say in a description, try answering all of the following
questions that are relevant:

- What is it?
- What does it do if it succeeds? What does it do if it fails? What can cause it to fail, and how?
- Is it idempotent?
- What are the units? (Examples: meters, degrees, pixels.)
- What range of values does it accept? Is the range inclusive or exclusive?
- What are the side effects?
- How do you use it?
- What are common errors that may break it?
- Is it always present? (For example: "Container for voting information. Present only when voting information is recorded.")
- Does it have a default setting?

## Sayings I Like

These are from various places and may be misremembered.

- Your work shapes your tools and your tools shape your work
- There that scattereth and yet increaseth
- The worker is worthy of his wages.
- Every line of code is a business decision
- Ten hours of coding can save one hour of reading.
- People with responsibilities have lives with meaning
- Use threads if you want to work in parallel, async if you want to wait in parallel
- People remember and make time for the things that are important to them. What is important to you?
- Men's lives are measured in works, not years! - a probably misremembered quote like this in Westminster Cathedral
- If you don't make mistakes, you're not working on hard enough problems. - Frank Wilczek
- The goal of refactoring is to increase the number of constraints that guide your program through your problem space. - paraphrased from [Jonathon Blow](https://www.youtube.com/watch?v=2J-HIh3kXCQ)
- If you’re overthinking, write. If you’re underthinking, read. - [Alex & Books](https://twitter.com/alexandbooks_/status/1446883211393503232?lang=en)
- Write code. Not too much. Mostly functions. - [Brandon.me](https://www.brandons.me/blog/write-code-not-too-much-mostly-functions)
- Prioritize impact over output
- Focus is what you say "no" to - paraphrased from [Steve Jobs](https://www.goodreads.com/quotes/629613-people-think-focus-means-saying-yes-to-the-thing-you-ve)

## Lessons from maintaining software over time

These are (pretty obvious) lessons slowly being beaten into me as I maintain personal and work projects over years. Some of these are pretty idealistic, and I'm still working to bring several of my projects up to these standards.

- Iteration speed is key! Being forced to wait for changes to deploy kills my motivation
- Don't build long-lived systems on new tech without strong justification! The team will forget how the new tech works and it'll be hell to keep up to date. We just got a ticket about some job failing that is built on tech I've never used. Someone on my team is going to have to learn that whole foreign ecosystem just to update this failing job. As another example, this is why I'm hesitant to introduce a Go project to my team. Most of our code is Python and we all generally know how Python works. I'm nervous that introducing Go and the suite of tools needed to use Go productively (editor plugins, linters, CI/CD config, etc.) without enthusiastic support from the team will make any Go code rot over time without my personal involvement. It's probably more maintainable to firm up the Python code CI/CD for code standards instead.
- You shouldn't be building systems you don't use regularly. Otherwise the code will rot.
- Minimize dependencies! Each dependency will probably need be updated and each update will need to be tested against your code. It's probably worth an extra 100 lines of code to do something instead of taking on a dependency. "A little copying is better than a little dependency". Of course, if you're copying that 100 lines of code between projects multiple times, it's probably worth using the same dependency in the projects instead. I still haven't figured out how to keep JavaScript apps maintainable over years.
- Continuous Integration is a must. Dependencies and any other changes become easier to manage with automatic testing. Ideally, tests/lints should be configured in the Git platform, in a git pre-commit hook, and via editor plugin. Linters should have a "auto-fix" option for things that make sense (like formatting). Linters should be easy to install and keep up to date (they are ALSO dependencies).
- After a codebase's general architecture has been established, commits should strive to be a ["perfect commit"](https://simonwillison.net/2022/Oct/29/the-perfect-commit/) with tests and docs included. Of course, while still prototyping the architecture, or for small changes, it might not be worth adding tests and docs to interfaces that will change.
- For in-house libraries where you control the library and all users of the library, breaking changes to the library should be quickly followed by updates to all clients using the library. It should generally be the library author responsible for updating the clients so they can feel the impact of the breaking change. If that's not possible, a changelog should be carefully kept up to date. Otherwise, you'll have to keep how multiple versions of the library function in your head while doing work.

