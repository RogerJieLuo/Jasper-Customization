# -*- coding: utf-8-*-
'''
    Connect to Wordpress
'''
from wordpress_xmlrpc import Client
from wordpress_xmlrpc import WordPressPost
from wordpress_xmlrpc.methods import posts

class Wordpresspost(object):

    def __init__(self):
        self.wp_url = "http://www.website.com/xmlrpc.php"
        self.wp_username = "username"
        self.wp_password = "password"
        self.wordpress = Client(self.wp_url, self.wp_username, self.wp_password)
        #self.wp_blogid = ""

    def createPost(self, post_title, post_content):
        # create draft
        post = WordPressPost()
        post.title = post_title
        post.content = post_content
        post.id = self.wordpress.call(posts.NewPost(post))
        # set status to be update
        #post.post_status = 'publish'
        #self.wordpress.call(posts.EditPost(post.id, post))

        return post

    def getAllPosts(self):
        '''
            get all the posts
        '''
        ps = self.wordpress.call(posts.GetPosts())
        #for post in ps:
            #print "title: %s, id %s " % (post.title, post.id)
        return ps

    def getThePost(self, post_id):
        post = self.wordpress.call(posts.GetPost(post_id))
        #print post.content
        return post

    def editPost(self, post_id, post_content, status):
        '''
        Args:
            post_id:
            post_content:
            status: publish OR draft
        Returns:
        '''
        post_id = 18
        post = self.wordpress.call(posts.GetPost(post_id))
        post.content = post_content
        post.post_status = status
        # save the change to the post
        self.wordpress.call(posts.EditPost(post.id, post))
        #print "Resume title: %s, the content: %s" % (post.title,post.content)

    def publishPost(self, post_id):
        '''
            publish the post with post id
        '''
        post = self.wordpress.call(posts.GetPost(post_id))
        post.post_status = 'publish'
        self.wordpress.call(posts.EditPost(post.id, post))

    def unpublishPost(self, post_id):
        '''
            make the post draft, so it's not published
        '''
        post = self.getThePost(post_id)
        post.post_status = 'draft'
        self.wordpress.call(posts.EditPost(post.id, post))

'''
if __name__=="__main__":
    wordpress = Wordpresspost()
    #wordpress.createPost("Post 1", "This is a test posting 1.")
    #wordpress.getAllPosts()
    #wordpress.editPost(18, "Content change and update", "publish")
    wordpress.unpublishPost(18)
'''
