# MovieLiker
 [DRF project] MovieLiker
 : check movie list and leave your review/comments.

## Tech
- python 
- django REST framework 

<br>

## Features
### User
- User
   - Join/Login User 
   - Email Authentication (Celery)
   - Auth Token
   - update profile, delete account (IsOwnerOrReadOnly)
- Admin
   - admin page 

### Movie/Review
- Movie CRUD (IsAdminOrReadOnly)
- Actor CRUD (IsAdminOrReadOnly)
- Review CRUD (IsReviewOwnerOrReadOnly)
