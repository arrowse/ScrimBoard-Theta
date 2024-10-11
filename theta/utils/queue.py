
# Posts waiting to be updated
postQueue = []
# Posts currently being updated
postUpdateStack = []

def updatePost(postObject):
    """Called from the postQueue / postUpdateStack system if the queue has less than 6 posts in it and the incoming post is not a duplicate. See more in utils/queue.py."""
    postUpdateStack.insert(postObject)
    pass

# If the post queue has a post in it and the stack has less than 6 posts being processed,
# take the last post and process it UNLESS it is a duplicate of a post already being processed
while len(postQueue) > 0 and len(postUpdateStack) < 6:
    if postQueue[-1] in postUpdateStack:
        postQueue.insert(0, postQueue.pop(-1))
    updatePost(postQueue.pop(-1))