## Clinician Booking App:

Functional Requirements:
1. User will be able to Create account.
2. Clinicians info like name, ph no, availability.
3. There will be a central availability and every clinician record created
    would then have those availabilities too.
4. User will be able to view a clinician's availability.
5. User will be able to book a clinician's timing.
6. User will be able to view their booking(s).
7. User will be able to cancel a clinician's booking. If done so,
    then that time should be shown again as available for the clinician.
8. Clinician will be able to cancel a booking or close a slot for any
    day.


## My thought process:
create an availability table which will have general timings. 
there will be a doctor's availability table having availability particular to a doc.
there will be a booking table/appointment table.

clinician and patients will be separate tables with onetoonefield mapping with the User table