from app import create_app
from common.database import db
from common import models

db.session.commit()
db.drop_all()
db.create_all()

admin = models.Role(role="admin", description="superadmin of the app")
ctm = models.Role(role="ctm", description="Course Team Member")
im = models.Role(role="im", description="Management")
stu = models.Role(role="student", description="Student")

db.session.add(admin)
db.session.add(ctm)
db.session.add(im)
db.session.add(stu)
db.session.commit()

u1 = models.User(name="A Student", email="abc@xyz.com", role=[stu])
u1.set_password("abcd")
u1.save()

#db.session.add(models.User(name="An Admin", email="admin@xyz.com", password=hash_password("abcd"), role=[admin]))
#db.session.add(models.User(name="A CTM", email="ctm@xyz.com", password=hash_password("abcd"), role=[ctm]))
#db.session.add(models.User(name="A Management", email="im@xyz.com", password=hash_password("abcd"), role=[im]))
#db.session.commit()