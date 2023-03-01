{
    'name': "Hospital Management System",
    'version':"16",
    'sequence':'-10', # where it shows in the apps 
    'summary': """ This module will manage all the hospital aspects """,
    'description': """ This module will manage all the hospital aspects """,
    'author': "Murtaja",
    'website': "https://murtaja.netlify.app",
    'category': 'Hospital',
    'version': '16.0',
    # when we use another module in our module we have to add it as a dependency.
    'depends': ['base','mail', 'sale'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'wizard/create_appointment_wizard.xml',
        'wizard/search_appointment_wizard.xml',
        'views/sale.xml',
        'views/views.xml',
        'views/doctor_view.xml',
        'views/hospital_patient.xml',
        'views/appointment_view.xml',
        'views/partner.xml',
        'report/report.xml',
        'report/patient_details.xml',
    ],
    'license': 'Other proprietary',
    'application': True # consider it as an application.
}