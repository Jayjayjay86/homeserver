# Home Server App

The Home Server App is a Django-based web application that serves as a local home server for hosting one or more React apps. It utilizes Gunicorn as a production-ready server and is designed for easy deployment on your local WiFi network. This app is a convenient solution for hosting personal React projects and experimenting with web development.

## Features

- Host one or more React apps on your local WiFi network.
- Utilize Gunicorn for serving the Django application.
- Easy deployment and setup process.

## Technologies Used

- **Django:** Backend web framework for managing hosting and serving React apps.
- **React:** Frontend JavaScript library for building user interfaces.
- **Gunicorn:** Production-ready WSGI HTTP server for deploying Django apps.
- **Nginx:** High-performance web server and reverse proxy (to be set up later for production).
- **HTML, CSS:** For structuring and styling the user interface.

## Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/jayjayjay86/home-server-app.git
   cd home-server-app
   ```

2. Install Django dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up your React apps inside the Django project's directory.

4. Start Gunicorn server:

   ```bash
   gunicorn project_name.wsgi
   ```

   Replace `project_name` with the name of your Django project.

5. Access your React apps:

   Open a web browser and navigate to `http://localhost:8000` to access your Django project and hosted React apps.

## Deployment

To deploy your Home Server App in a more production-ready manner, consider setting up Nginx as a reverse proxy. Here's a high-level overview:

1. Install and configure Nginx on your server.

2. Set up a new Nginx server block (virtual host) that forwards requests to your Gunicorn server.

3. Configure Gunicorn to run your Django app using the `gunicorn` command and bind it to a socket.

4. Update your Django settings to use the `ALLOWED_HOSTS` list to specify the domains that can access your app.

5. Secure your server using HTTPS, possibly using Let's Encrypt.

## Contributing

Contributions to the Home Server App are welcome! Feel free to open issues and submit pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to the Django and React communities for their invaluable tools and resources.

---

Please replace placeholders such as `your-username`, `project_name`, and customize the instructions according to your project structure and setup. Make sure to consult the official documentation of Django, Gunicorn, and Nginx for more detailed setup and deployment instructions.
