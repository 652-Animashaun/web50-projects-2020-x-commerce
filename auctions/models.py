from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Listing(models.Model):
	title = models.CharField(max_length=64)
	description = models.CharField(max_length=200)
	imageUrl = models.URLField()
	initialBid = models.IntegerField()
	vendor= models.ForeignKey(User, on_delete=models.CASCADE, related_name="vendor", default=1)
	highestBid= models.IntegerField(default=0, null=True)
	category= models.CharField(max_length=64, default="uncategorized")
	highestBidder= models.ForeignKey('Bid', on_delete=models.DO_NOTHING, default=None, null=True)
	is_active = models.BooleanField(default=True)
	
	
	

	def __str__(self):
		return f"{self.id} : {self.title} \n Description: {self.description} \n Current Bid: ${self.initialBid} \n Seller: {self.vendor}"

class Bid(models.Model):
	listingId= models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bidItem")
	currBid = models.IntegerField()
	bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidder", default=None, null=True )



class Comments(models.Model):
	userId = models.ForeignKey(User, on_delete=models.CASCADE, related_name="usercomment")
	comment= models.CharField(max_length=200)
	listingId= models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="UserListingComment")

	def __str__(self):
		return f"{self.userId} wrote: \n {self.comment} "

class UserProfile(models.Model):
	userId = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
	shipping = models.CharField(max_length=200)

class Watchlist(models.Model):
	listingId=models.ForeignKey(Listing, on_delete=models.CASCADE)
	userId=models.ForeignKey(User, on_delete=models.CASCADE)
