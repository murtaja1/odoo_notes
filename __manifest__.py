{
    'name': "Hospital Management System",
    'version':"16",
    'summary': """ This module will manage all the hospital aspects """,
    'description': """ This module will manage all the hospital aspects """,
    'author': "Murtaja",
    'website': "https://murtaja.netlify.app",
    'category': 'Hospital',
    'version': '16.0',
    'depends': ['base','mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/views.xml',
        'views/hospital_patient.xml',
    ],
    'license': 'Other proprietary',
    # 'application': True # consider it as an application.
}