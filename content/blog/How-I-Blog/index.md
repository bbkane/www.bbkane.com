+++
title = "How I Blog"
date = 2015-03-23
updated = 2016-12-25
aliases = [ "2015/03/23/How-I-Blog.html" ]
+++

Here are some notes about making blog posts (especially easily adding images).

- posts are in the `\_posts/` folder.
- a post must be named according to the date and then the title of the post: `\_posts/2015-03-23-Title-Name-Here.md`
- a post's images are in the `images/post\_name` folder: `images/2015-03-23-Title-Name-Here/image\_name.png`
- A post must contain the following insert at the top:

```
---
layout: default
title: My Title Here
---
```

- I write Markdown using [HarooPad](http://pad.haroopress.com/user.html)
- I capture images useing [Sharex](https://github.com/ShareX/ShareX)
- I automate the process with [AutoHotkey](http://ahkscript.org/)
- I use the following settings on Sharex:
![](./ShareX_9.7_2015-03-23_12-34-33.png)
- I've also set the hotheys to `F1` (capture active window) and `F2` (capture rectangle) for convenience

- Now that I've got Sharex set up, I need to automate generating an image link. I do this with an AutoHotkey script

```
; This script sets up a path when first run.
; Then, it waits for a file path to be copied to the clipboard
; and changes it to a markdown image link,
; which is returned to the clipboard
; I want to use it with Sharex on the following settings:
; After Capture: check "save image to file as" and
; "copy file path to clipboard"
; Hotkey settings can also be manipulated to facilitate
; easy image capturing

#Persistent ; stay in background, waiting
InputBox, folder_name, Enter folder name (minus final slash): , For my blog it is usually "{{ site.baseurl }}/img/YYYY-MM-DD-Title-Here" (and create that folder if it doesn't exist) ; TODO: Get AutoHotkey to make folder, post, and format them
return ; when first run, do nothing but set up folder

; wait for clipboard to change
OnClipboardChange:
; get contents of clipboard
full_file_name := clipboard

; is it a valid path?
is_file_path := RegExMatch(full_file_name, "(.*):\\")
if (is_file_path = 1) {
	; extract file name from path
	SplitPath, full_file_name, file_name
	image_link = ![](%folder_name%/%file_name%)
	clipboard := image_link
}
```

- Running the script yields:

![](./inputbox.png)

- Now, when I push F1, it asks to save the image. I do that in its folder (the one under images, remember), and hit Ctrl-V to paste the image link into my editor. Here's one right now!
![](./rightnow.png)

- Unfortunately, Github Pages doesn't like links that return to a parent folder. The last step, then, is to change `../images` to `\{\{ site.baseurl \}\}/images` (without the backslashes). This is a simple Find and Replace operation.
- Push the post and images to Github.
- Check the generated webpage and edit any errors.

# Update

After writing this, I updated my script to this:

```
#Persistent ; stay in background, waiting

; set root directory
str_root_dir = E:\Blog\bbk1524.github.io

; set path for haroopad
str_md_editor = E:\Portable Programs\Haroopad\haroopad.exe

; set path for Sharex
str_image_capturer = C:\Program Files\ShareX\Sharex.exe

; get title
InputBox, str_blog_title, Enter Title of Blog, Title should be separated by spaces

; create str_dashed_title to replace spaces
StringReplace, str_dashed_title, str_blog_title, %A_Space%, -, All

; add the date
str_full_title = %A_YYYY%-%A_MM%-%A_DD%-%str_dashed_title%

; set directory for posts
str_post_dir = %str_root_dir%\_posts

; make post with the boilerplate
FileAppend, ---`nlayout: post`ntitle: %str_blog_title%`n---`n`n, %str_post_dir%\%str_full_title%.md

;start Haroopad
Run, %str_md_editor% %str_post_dir%\%str_full_title%.md


; If I don't want images, then exit the app
MsgBox, 4,, Will this post include images?
ifMsgBox No
	ExitApp

; make an image subdirectory for this post
str_image_dir = %str_root_dir%\images\%str_full_title%
FileCreateDir, %str_image_dir%

; run ShareX
Run, %str_image_capturer%

; make it so Haroopad can see the files (NOTE: this depends on the folder heirarchy, might want to make more generic... later)
str_put_image_here = ../img/%str_full_title%

; when first run, do nothing but set up folder and post
return

; wait for clipboard to change
OnClipboardChange:
; get contents of clipboard
str_full_file_name := clipboard

; Only change it if it's a valid path
is_file_path := RegExMatch(str_full_file_name, "(.*):\\")
if (is_file_path = 1) {
	; extract file name from path
	SplitPath, str_full_file_name, file_name
	image_link = ![](%str_put_image_here%/%file_name%)
	clipboard := image_link
}
```

So the process has now been considerably shortened to:

- Run script
- Enter title of post
- Decide whether it should include images or not
- if including images, make sure Sharex's setting are correct
- Don't forget to save images in the correct image directory
- Blog
- Replace image urls
- Push and edit
