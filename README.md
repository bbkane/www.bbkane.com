# My Site!

Really liking Zola! I can build this locally with `zola serve`!

# TODO

- add create_post script
- Site Analytics - https://github.com/piratepx/app , https://counter.dev/ , https://www.goatcounter.com/
- Get search working (put in home page)
- RSS feed
- TELL PEOPLE TO EMAIL ME IF THEY LIKE MY BLOG POSTS!!
- Get "view page source" on GitHub - see https://tera.netlify.app/docs/#macros for macros
- Use page.relative_path to add "Edit on Github" link (wish I could use current_path)
- Get twitter, reddit, LI pipeline
- fix blog up with mozilla

# Done

- get word count - done
- port mds - done
- Get Google Site-Analytics working - done
- get root page working - done
- get code blocks not one-liners - done
- get content truncated in index - done
- get empty links filled `/\[.*\]()` - done
- Sort by updated not working?? - made https://github.com/getzola/zola/issues/1384 to try to get this supported
- Why does zola serve work but zola build not? - HTML expects a root. Building and starting a local server in that directory fixes this.
- figure out how to use images. Test site? See https://www.getzola.org/documentation/content/overview/#asset-colocation
- make sure all vars work on old blog- all of them are for the `{{ site.baseurl }}/path/to/image`
- Is code CSS not working anymore? It looks like it's using a zola built-in one. Rm the original CSS
- port /img/favicon/... images (not sure where they're needed?)
- Push to netlify!
