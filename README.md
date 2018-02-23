## 360 Camera account DB model v1.0

### table
    - User
    - Camera
    - CameraFriend
    - Cars
    - Domain
    - ProductSerial

---

#### User

Registed user. 

label:

    - email
    - first_name
    - last_name
    - sex
    - register_date
    - modify_date
    - friend (Many to Many)

#### Camera

Camera information

label:

    - user (owner Many to One)
    - sn
    - bind_at
    - fob_num
    - name
    - domain (upload gps, fob to amazon server domain name)

#### CameraFriend

can get alert and stream besides owner.

label:

    - camera (camera, Many to Many)
    - friend (User, Many to One)
    - is_active (true -> can get alert and streaming)

#### Cars

Car information which use 360 camera.

label:

    - license_plate
    - color
    - brand
    - owner (User, Many to One)

#### ProductSerial

our product serial data.

label:

    - sn
    - be_used
