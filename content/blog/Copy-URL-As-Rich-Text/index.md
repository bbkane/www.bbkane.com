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

So, without further ado, here's the bookmarklet I'm now using to copy the title and URL from a page. It writes a minimal HTML link to the clipboard, without copying the page's styling, so the pasted link uses the destination document's style.

Drag this link to your bookmarks bar:

<a href='javascript:(async()=>{const t=document.title,u=location.href,a=document.createElement("a");a.href=u;a.textContent=t;const h=a.outerHTML,p=`${t} - ${u}`;try{await navigator.clipboard.write([new ClipboardItem({"text/html":new Blob([h],{type:"text/html"}),"text/plain":new Blob([p],{type:"text/plain"})})])}catch(e){prompt("Rich-text copy failed. Copy this instead:",p)}})();'>Title Link RTF</a>

```javascript
javascript:(async () => {
    const title = document.title;
    const url = location.href;
    const link = document.createElement("a");
    link.href = url;
    link.textContent = title;

    const html = link.outerHTML;
    const plainText = `${title} - ${url}`;

    try {
        await navigator.clipboard.write([
            new ClipboardItem({
                "text/html": new Blob([html], { type: "text/html" }),
                "text/plain": new Blob([plainText], { type: "text/plain" }),
            }),
        ]);
    } catch (error) {
        prompt("Rich-text copy failed. Copy this instead:", plainText);
    }
})();
```
