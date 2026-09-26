from abc import ABC, abstractmethod

#abstract Basis class
class Person(ABC):
    def __init__(self, name):
        self.name = name

    #jede unterklasse muss diese Methode implementieren
    @abstractmethod
    def get_info(self):
        pass

class Patients(Person):
    def __init__(self, name, age, gender, phone, address):
        super().__init__(name)
        self.age = age
        self.gender = gender 
        self.phone = phone
        self.address = address

# Getter-Methode für das Alter und Validierung 
    @property
    def age(self):
        return self._age

# Setter-Methode für das Alter mit Validierung
    @age.setter
    def age(self, value):
        if not isinstance(value, int) or value < 0:
            raise ValueError("Age cannot be String or negative.")
        self._age = value

    def get_patient_info(self):
        return self.name, self.age, self.gender, self.phone, self.address
    
# Implementierung der abstrakten Methode get_info
    def get_info(self):
        return self.get_patient_info()

class Doctors(Person):
    def __init__(self, name, specialization, available, salary):
        super().__init__(name)
        self.specialization = specialization
        self.available = available      
        self.salary = salary

    def get_doctor_info(self):
        return self.name, self.specialization, self.available, self.salary
    
# Implementierung der abstrakten Methode get_info
    def get_info(self):
        return self.get_doctor_info()

class Appointments:
    def __init__(self, patient_name, doctor_name, date, time):
        self.patient_name = patient_name
        self.doctor_name = doctor_name
        self.date = date
        self.time = time

    def get_appointment_info(self):
        return self.patient_name, self.doctor_name, self.date, self.time

class Nurses(Person):
        def __init__(self, name, department, shift):
            super().__init__(name)
            self.department = department
            self.shift = shift

        def get_nurse_info(self):
            return self.name, self.department, self.shift

# Implementierung der abstrakten Methode get_info
        def get_info(self):
            return self.get_nurse_info()

class Medicines:
        def __init__(self, name, quantity, price):
            self.name = name
            self.quantity = quantity
            self.price = price

        def get_medicine_info(self):
            return self.name, self.quantity, self.price
        
class LaboratoryTests:
        def __init__(self, name, test_type, price):
            self.name = name
            self.test_type = test_type
            self.price = price

        def get_test_info(self):
            return self.name, self.test_type, self.price

class Expenses:
        def __init__(self, expense_type, amount):
            self.expense_type = expense_type
            self.amount = amount

        def get_expense_info(self):
            return self.expense_type, self.amount

class Roles:
        def __init__(self, role_name, permissions):
            self.role_name = role_name
            self.permissions = permissions

        def get_role_info(self):
            return self.role_name, self.permissions


class ManagementSystem:

    def __init__(self):
        self.patients = []
        self.doctors = []
        self.appointments = []
        self.Nurses = []
        self.medicines = []
        self.laboratory_tests = []
        self.Expenses = []
        self.Roles = []
        

    def add_patient(self, patient):
        self.patients.append(patient)

    def find_patient(self, name):
        for patient in self.patients:
            if patient.name == name:
                return patient
        return None

    def update_patient(self, name, new_info):
        patient = self.find_patient(name)
        if patient:
            patient.name = new_info.get("name", patient.name)
            patient.age = new_info.get("age", patient.age)
            patient.gender = new_info.get("gender", patient.gender)
            patient.phone = new_info.get("phone", patient.phone)
            patient.address = new_info.get("address", patient.address)
            return True
        return False

    def remove_patient(self, name):
        patient = self.find_patient(name)
        if patient:
            self.patients.remove(patient)
            return True
        return False

    def add_doctor(self, doctor):
        self.doctors.append(doctor)

    def find_doctor(self, name):
        for doctor in self.doctors:
            if doctor.name == name:
                return doctor
        return None

    def update_doctor(self, name, new_info):
        doctor = self.find_doctor(name)
        if doctor:
            doctor.name = new_info.get("name", doctor.name)
            doctor.specialization = new_info.get("specialization", doctor.specialization)
            doctor.available = new_info.get("available", doctor.available)
            doctor.salary = new_info.get("salary", doctor.salary)
            return True
        return False

    def remove_doctor(self, name):
        doctor = self.find_doctor(name)
        if doctor:
            self.doctors.remove(doctor)
            return True
        return False


    def add_appointment(self, appointment):
        self.appointments.append(appointment)

    def find_appointment(self, patient_name, doctor_name):
        for appointment in self.appointments:
            if appointment.patient_name == patient_name and appointment.doctor_name == doctor_name:
                return appointment
        return None

    def cancel_appointment(self, patient_name, doctor_name):
        appointment = self.find_appointment(patient_name, doctor_name)
        if appointment:
            self.appointments.remove(appointment)
            return True
        return False

    def update_appointment(self, patient_name, doctor_name, new_info):
        appointment = self.find_appointment(patient_name, doctor_name)
        if appointment:
            appointment.date = new_info.get("date", appointment.date)
            appointment.time = new_info.get("time", appointment.time)
            return True
        return False
    
    
    def add_nurse(self, nurse):
        self.Nurses.append(nurse)

    def find_nurse(self, name):
        for nurse in self.Nurses:
            if nurse.name == name:
                return nurse
        return None

    def update_nurse(self, name, new_info): 
        nurse = self.find_nurse(name)
        if nurse:
            nurse.name = new_info.get("name", nurse.name)
            nurse.department = new_info.get("department", nurse.department)
            nurse.shift = new_info.get("shift", nurse.shift)
            return True
        return False

    def remove_nurse(self, name):
        nurse = self.find_nurse(name)
        if nurse:
            self.Nurses.remove(nurse)
            return True
        return False
    

    def add_medicine(self, medicine):
        self.medicines.append(medicine)

    def find_medicine(self, name):
        for medicine in self.medicines:
            if medicine.name == name:
                return medicine
        return None

    def update_medicine(self, name, new_info):
        medicine = self.find_medicine(name)
        if medicine:
            medicine.name = new_info.get("name", medicine.name)
            medicine.quantity = new_info.get("quantity", medicine.quantity)
            medicine.price = new_info.get("price", medicine.price)
            return True
        return False

    def remove_medicine(self, name):
        medicine = self.find_medicine(name)
        if medicine:
            self.medicines.remove(medicine)
            return True
        return False

    
    def add_laboratory_test(self, laboratory_test):
        self.laboratory_tests.append(laboratory_test)

    def find_laboratory_test(self, name):
        for laboratory_test in self.laboratory_tests:
            if laboratory_test.name == name:
                return laboratory_test
        return None

    def update_laboratory_test(self, name, new_info):
        laboratory_test = self.find_laboratory_test(name)
        if laboratory_test:
            laboratory_test.name = new_info.get("name", laboratory_test.name)
            laboratory_test.test_type = new_info.get("test_type", laboratory_test.test_type)
            laboratory_test.price = new_info.get("price", laboratory_test.price)
            return True
        return False

    def remove_laboratory_test(self, name):
        laboratory_test = self.find_laboratory_test(name)
        if laboratory_test:
            self.laboratory_tests.remove(laboratory_test)
            return True
        return False
    

    def add_expense(self, expense):
        self.Expenses.append(expense)

    def find_expense(self, expense_type):   
        for expense in self.Expenses:
            if expense.expense_type == expense_type:
                return expense
        return None

    def update_expense(self, expense_type, new_info):
        expense = self.find_expense(expense_type)
        if expense:
            expense.expense_type = new_info.get("expense_type", expense.expense_type)
            expense.amount = new_info.get("amount", expense.amount)
            return True
        return False

    def remove_expense(self, expense_type):
        expense = self.find_expense(expense_type)
        if expense:
            self.Expenses.remove(expense)
            return True
        return False
    

    def add_role(self, role):
        self.Roles.append(role)

    def find_role(self, role_name):  
        for role in self.Roles:
            if role.role_name == role_name:
                return role
        return None 

    def update_role(self, role_name, new_info): 
        role = self.find_role(role_name)
        if role:
            role.role_name = new_info.get("role_name", role.role_name)
            role.permissions = new_info.get("permissions", role.permissions)
            return True
        return False    

    def remove_role(self, role_name):   
        role = self.find_role(role_name)
        if role:
            self.Roles.remove(role)
            return True
        return False

         
    def get_patients(self):
        return self.patients

    def get_doctors(self):
        return self.doctors

    def get_appointments(self):
        return self.appointments

    def get_nurses(self):
        return self.Nurses

    def get_medicines(self):
        return self.medicines   

    def get_laboratory_tests(self):
        return self.laboratory_tests    

    def get_expenses(self):
        return self.Expenses    

    def get_roles(self):
        return self.Roles


#inheritance example

# Ein Patientenobjekt erstellen
patient1 = Patients("Ali", 30, "Male", "12345", "Essen")

# Den geerbten Namen ausgeben
print(patient1.name)

# Das Alter des Patienten ausgeben
print(patient1.age)

# Alle Patientendaten ausgeben
print(patient1.get_patient_info())

# Überprüfen, ob Patients von Person erbt
print(isinstance(patient1, Person))

#######################################
#Encapsulation example

patient1 = Patients("Mo Doe", 30, "Male", "1234567890", "123 Main St")

patient1.age = 31  # Valid age assignment
print(patient1.age)  # Output: 31

# Invalid age assignment
try:
    patient1.age = -5  # This will raise a ValueError
except ValueError as e:
    print(e)  # Output: Age cannot be String or negative.
##############################################

#polymorphism example

patient = Patients("John Doe", 30, "Male", "1234567890", "123 Main St")
doctor = Doctors("Dr. Smith", "Cardiology", True, 100000)
nurse = Nurses("Nurse Jane", "Pediatrics", "Day")

persons = [patient, doctor, nurse]

for person in persons:
    print(person.get_info())  # Calls the appropriate get_info method based on the object type

#############################################

# Abstract class example


# Eine Person direkt erstellen
try:
    person = Person("Ali")
except TypeError:
    print("Person kann nicht direkt erstellt werden")

# Einen Patienten erstellen
patient = Patients("Ali", 30, "Male", "12345", "Essen")

# Die abstrakte Methode ist in Patients implementiert
print(patient.get_info())

#####################################################