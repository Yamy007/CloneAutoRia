## API CloneAutoRia

### Users

-   **auth**

    1. **RegisterUser**: Ordinary platform users can register with their email, password, and some personal information.
    2. **RegisterUserAsSeller**: Similar to RegisterUser, but with a different endpoint, marking the account as a seller.
    3. **RegisterAdminUser**: Accessible only to the site owner, allowing registration of admin accounts.
    4. **login**: Enter email and password to receive two tokens, access, and refresh.
    5. **ActivateAccount**: Use the token received via email during registration to activate the account.

-   **settings**

    1. **updateUser**: Site owners can transform regular users into admins, activate accounts, or block users.
    2. **updateUserProfile**: User-specific API for adding photos and changing profiles.
    3. **updateUserProfileById**: Site owners can update profiles of other users by their ID.

-   **show**

    1. **AllUsers**: Retrieve all users, accessible only to admins.
    2. **UserById**: Retrieve a user by their ID, accessible only to admins.
    3. **GetMeUser**: Retrieve data about oneself.

-   **block**

    1. **BlockUser**: Admins can block a user by their ID.
    2. **UnBlockUser**: Admins can unblock a user by their ID.

-   **premium**
    1. **AddPremium**: After payment, admins grant premium status to users; specify the number of days (taken from the CreatePremiumTime API).
    2. **DeletePremium**: Admins can remove premium status.
    3. **GetPremiumTime**: Retrieve a list of all premium types (number of days and price), accessible only to admins.
    4. **CreatePremiumTime**: Create a new premium type, accessible only to admins.
    5. **DestroyPremium**: Delete unnecessary premium types, accessible only to admins.
    6. **SetPremiumTime**: Configure premium types, accessible only to admins.

### Cars (Admin Only)

(Cars are an abstract entity for creating advertisements, designed to prevent users from creating non-existent models like Audi or x5. Users can only choose from existing cars in the database.)

1. **getAllCars**: API that returns all created cars.
2. **createCars**: API for creating cars.
3. **getCarsById**: API to retrieve a car by its ID.
4. **updateCarsById**: API for editing existing cars.
5. **delete**: API for deleting cars.

### Advertisement

1. **createAdvertimes**: API available only for SELLERS, allowing the creation of advertisements; by default, the advertisement will be inactive.
2. **getAllAdvertisement**: API to view all advertisements (accessible to anyone).
3. **retrieveAdverById**: API to view an advertisement by ID; if the advertisement is inactive, it is only accessible to the owner.
4. **updateDescription**: API to update the description of a car.
5. **destroy**: API for deleting an advertisement, accessible only to the owner or admins.
6. **addImageByAdvert**: API for adding photos to an advertisement; unlimited photos can be added.
7. **view**: API to add views (accessible only to logged-in users); one user view equals one count.
8. **courseNow**: Returns the current exchange rate from PrivatBank.
9. **activateAdvert**: API for activating advertisements; after 3 failed attempts, admins receive an email to review the problematic advertisement.
10. **staticViews**: View statistics; accepts date range parameters.
11. **staticAvg**: Average price statistics; all=True for all regions, all=False for region-specific data; includes type_price for average price in a specific currency.

### Languages and Tools :

<div>
  <img src="https://github.com/devicons/devicon/blob/master/icons/python/python-original-wordmark.svg" title="Python" alt="Python" width="60" height="60"/>&nbsp;
  <img src="https://github.com/devicons/devicon/blob/master/icons/django/django-plain-wordmark.svg" title="Django" alt="Django " width="60" height="60"/>&nbsp;
<img src="https://github.com/devicons/devicon/blob/master/icons/vscode/vscode-original.svg" title="VScode" alt="VScode" width="60" height="60"/>&nbsp;
</div>

## Easy Start

```bash
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python runserver
```
