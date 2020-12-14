Base.metadata.create_all(engine)         #create all the tables frames

#-----------example check----------------------------
session.add_all([Rating(name='positive'), Rating(name='negative')])
session.commit()


create_user(session, 'jon', 'jon@domain.com', '12345')
create_user(session, 'manny', 'manny@domain.com', 'manymen')
create_user(session, 'dror', "drorbiton98@gmail.com", 'd123456B')

u1 = session.query(User).filter(User.name == 'jon').first()
u2 = session.query(User).filter(User.name == 'manny').first()
u3 = session.query(User).filter(User.name == 'dror').first()

post(session, u3.id, 'first post', 'hello my frieds')
post(session, u1.id, 'u wont be live it', 'ha ha funny lol')
post(session, u2.id, 'do you like sleep', 'i want it')
post(session, u3.id, 'second post', 'third time i scream for help')
post(session, u3.id, 'first 1', '1')
post(session, u3.id, 'first 2', '2')
post(session, u3.id, 'first 3', '3')
post(session, u3.id, 'first 4', '4')
post(session, u3.id, 'first 5', '5')


p1 = session.query(Post).filter(Post.title == 'first post').first()
p2 = session.query(Post).filter(Post.title == 'u wont be live it').first()
p3 = session.query(Post).filter(Post.title == 'do you like sleep').first()
p4 = session.query(Post).filter(Post.title == 'second post').first()


comment(session, p1.id, u2.id, 'hello brother', 1)
comment(session, p1.id, u1.id, 'hey man', 1)
comment(session, p3.id, u3.id, 'yes my friend very much', 1)