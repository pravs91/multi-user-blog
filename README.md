# multi-user-blog
A webapp for a blogging site. Can be accessed at https://pravs-blogstop.appspot.com
Deployed on Google Cloud Platform.

# Features
- Create user accounts
- Login/ logout functionality.
- Saved sessions using cookies. Logged-in users need not have to login again.
- Create, edit and delete blog posts for logged-in users.
- Logged-in users can like/unlike posts, but not on their own posts
- Logged-in users can create, edit and delete comments on blog posts.
- Users can only Edit/delete their own posts

# URL routing (sub-domains)
- /blog - blog main page with all posts in descending order
- /blog/login - Login page
- /blog/signup - Signup page
- /blog/logout - Logout page
- /blog/welcome - Welcome page for a user showing their own posts
- /blog/newpost - Create a new post for current user
- /blog/<blog_id> - Permanent link for a particular blog page.
- /blog/<blog_id>/edit - Edit a blog
- /blog/<blog_id>/delete - Delete a blog
- /blog/<blog_id>/createComment - Create comment for a blog
- /blog/<comment_id>/editComment - Edit a comment
- /blog/<comment_id>/deleteComment - Delete a comment
- /blog/<user_name>/ - Access a particular user's blog posts

# Deploying the app
Create new project in gcloud console (web) and run these commands:
```
gcloud config set project <project_name_on_gcloud>
gcloud beta app create
gcloud app deploy index.yaml
gcloud app deploy
```
