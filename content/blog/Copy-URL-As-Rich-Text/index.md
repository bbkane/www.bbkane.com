+++
title = "Copy URL as Rich Text"
date = 2023-08-01
+++

Last time I tried the MS Edge browser, I really liked the "copy URL from the address bar and get a rich text link containing the title and URL" feature. In contrast, copying the URL from the address bar in Firefox only gives you the URL text.

I ended up sticking with Firefox, but I copy links all the time into notes and documents, so getting good looking links to things is important to me.

# Markdown Formatted Link

 I found a [bookmarklet](https://gist.github.com/bradleybossard/3667ad5259045f839adc) that, when clicked, copies a markdown link, but the link is not rich text, and I didn't want to take the time trying to enable rich text links.

```javascript
javascript:(function() {
    function copyToClipboard(text) {
        if (window.clipboardData && window.clipboardData.setData) {
            /*IE specific code path to prevent textarea being shown while dialog is visible.*/
            return clipboardData.setData("Text", text);
        } else if (document.queryCommandSupported && document.queryCommandSupported("copy")) {
            var textarea = document.createElement("textarea");
            textarea.textContent = text;
            textarea.style.position = "fixed"; /* Prevent scrolling to bottom of page in MS Edge.*/
            document.body.appendChild(textarea);
            textarea.select();
            try {
                return document.execCommand("copy"); /* Security exception may be thrown by some browsers.*/
            } catch (ex) {
                console.warn("Copy to clipboard failed.", ex);
                return false;
            } finally {
                document.body.removeChild(textarea);
            }
        }
    }
    var markdown = '[' + document.title + '](' + window.location.href + ')';
    copyToClipboard(markdown);
})();
```

This works for most links but can only paste the markdown formatted plain text.

# Rich Text Link

Luckily, Simon Willison [wrote how to do this](https://til.simonwillison.net/javascript/copy-rich-text-to-clipboard), and I was able to easily use his function in my own bookmarklet.

So, without further ado, here's the bookmarklet I'm now using to copy the titla and the URL from a page. I've got it saved in my bookmarks bar, so I just click it and happily paste elsewhere.

Unfortunately, it doesn't seem to work on Google Docs links

```javascript
javascript:(function() {

    function copyRichText(html) {
        const htmlContent = html;
        /* Create a temporary element to hold the HTML content */
        const tempElement = document.createElement("div");
        tempElement.innerHTML = htmlContent;
        document.body.appendChild(tempElement);
        /* Select the HTML content */
        const range = document.createRange();
        range.selectNode(tempElement);
        /* Copy the selected HTML content to the clipboard */
        const selection = window.getSelection();
        selection.removeAllRanges();
        selection.addRange(range);
        document.execCommand("copy");
        selection.removeAllRanges();
        document.body.removeChild(tempElement);
    }

var link = `<a href="${window.location.href}">${document.title}</a>`;
copyRichText(link);
})();
```

