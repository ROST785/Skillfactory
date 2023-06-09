user_1 = User.objects.create_user(username='user_1')
user_2 = User.objects.create_user(username='user_2')
author_1 = Author.objects.create(user=user_1)
author_2 = Author.objects.create(user=user_2)
category_1 = Category.objects.create(category_name='category_1')
category_2 = Category.objects.create(category_name='category_2')
category_3 = Category.objects.create(category_name='category_3')
category_4 = Category.objects.create(category_name='category_4')
paper_1 = Post.objects.create(author=author_1, post_type='Статья', header='header_1', text='text_1')
paper_2 = Post.objects.create(author=author_2, post_type='Статья', header='header_2', text='text_2')
news_1 = Post.objects.create(author=author_1, post_type='Новости', header='header_3', text='text_3')
paper_1.categories.add(category_1, category_2)
paper_1.save()
paper_2.categories.add(category_2, category_3)
paper_2.save()
news_1.categories.add(category_2, category_4)
news_1.save()
comment_1 = Comment.objects.create(post=paper_1, user=user_2, text='text_1')
comment_2 = Comment.objects.create(post=paper_2, user=user_1, text='text_2')
comment_3 = Comment.objects.create(post=news_1, user=user_1, text='text_3')
comment_4 = Comment.objects.create(post=news_1, user=user_2, text='text_4')
paper_1.like()
paper_2.like()
news_1.dislike()
comment_1.like()
comment_2.dislike()
comment_3.like()
comment_4.dislike()
author_1.update_rating()
author_2.update_rating()
best_user = Author.objects.order_by('-rating').values('User__username', 'rating').first()
best_post = Post.objects.order_by('-rating').values('post_datetime', 'author__user__username', 'rating', 'header').first()
comments = Comment.objects.filter(post=best_post_for_for_preview).values('comment_datetime', 'user', 'rating', 'text')