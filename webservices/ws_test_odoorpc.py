import odoorpc

odoo = odoorpc.ODOO('localhost', port=8069)

print("1.- Base de Datos: ", odoo.db.list())

odoo.login('odoodb', 'admin', 'admin')
user = odoo.env.user
print("2.- odoo.env.user: ",user)

print("3.- Nombre de Usuario:", user.name)            # name of the user connected
print("4.- active", user.company_id.partner_id.name) # the name of its company


user_data = odoo.execute('res.users', 'read', [user.id], ['password'])
print("5.-",user_data)

user.name = 'moylop260'