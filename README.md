# eBay-like E-Commerce Auction Site

This project is an eBay-like e-commerce auction site developed using Django, allowing users to post auction listings, place bids on listings, comment on listings, and add listings to a watchlist.

![Active Listing Page](staticfiles\auctions\auction1.png)
![Listing Page](staticfiles\auctions\auction2.png)

## Features

- **User Authentication**: Secure registration and login functionality.
- **Listing Creation**: Users can create auction listings with titles, descriptions, starting bids, images, and categories.
- **Active Listings Page**: Displays all currently active auction listings with key details
- **Listing Page**: View detailed information about listings, place bids, comment, and add or remove items from the watchlist.
- **Watchlist**: Users can manage their personal watchlist of favorite listings.
**Comments**: Users can comment on listings and view all comments made.
- **Categories**: Explore listings by different categories.
- **Django Admin Interface**: Admin can manage listings, comments, and bids via the Django admin interface.

## Getting Started

#### Live Demo

- Visit <a href="https://commerce1.azurewebsites.net/" target="_blank"><b>e-commerce</b></a> in your browser to view the site.

#### Installation (Optional)

1. Clone the repository:

   ```bash
   git clone https://github.com/madefromjames/eBay-like_e-commerce_auction_site.git
   ```
2. Install dependencies:
    ```
    pip install -r requirements.txt
    ```
3. Make migrations and migrate the database:
    ```
    python manage.py makemigrations
    python manage.py migrate
    ```
#### Usage

1. To run the server:
    ```
    python manage.py server
    ```
    Visit http://127.0.0.1:8000 in your browser to view the site.

## Contributing
Contributions are welcome! Feel free to open issues or submit pull requests.
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit them (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request.

## Acknowledgments

- Thank you for visiting the eBay-like E-Commerce Auction Site repository. We hope you find this project interesting and useful. Your contributions and feedback are highly appreciated. Happy coding!🚀

- Special thanks to the CS50 team for providing the inspiration for this project.
---

**Note**: This project is part of the [CS50 Web Programming with Python and JavaScript](https://cs50.harvard.edu/web/2020/projects/2/commerce/#commerce) course by Harvard University.
