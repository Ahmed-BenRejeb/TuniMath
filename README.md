# YOUR PROJECT TITLE: TUNIMATH
#### Video Demo: [https://youtu.be/a2DnZhyhtwY]

#### Description:
As a second-year engineering student, I often faced difficulties when it came to verifying basic calculations and plotting graphs for various assignments and projects. This struggle led me to create this project with the goal of simplifying these tasks, particularly for students who might find themselves in the same situation I was in. The aim of this project is to provide an easy-to-use platform that combines essential mathematical tools and functionalities in one place, making it more accessible and efficient for students to perform calculations, solve equations, and visualize functions.

The project includes the following files:

- **app.py**: This file handles the routing and the core Flask functionalities, which control the flow of the application, linking the various pages together. It contains the logic for directing the user to different sections based on the actions they take.

- **helper.py**: This file includes the essential functions that power the application's backend, such as the login system, which verifies user credentials, and the mathematical functions used to perform calculations on the user's input.

- **project.db**: The database file stores user information, including a unique user ID, email, login time, and a securely hashed password. It is the foundation for the user authentication process, ensuring only authorized users can access the website.

The HTML files in the project provide the structure and layout for the user interface. They are designed to be intuitive and user-friendly, with functionality tailored to the project's features. These files include:

- **register.html**: A simple registration page where users can create an account to access the website. The page prompts for essential details, such as email and password, and stores the information in the database.

- **login.html**: This page allows registered users to log in. Upon submission, their credentials are checked against the database. If the details are correct, the user gains access to the platform; otherwise, a SweetAlert message will appear to inform them of the failure and prevent further access.

- **changepassword.html**: If users forget their password, they can use this page to reset it. While the feature does not yet include email notifications or two-factor authentication (2FA), users can change their password directly from this page. This feature is especially useful for users who may have forgotten their login details.

- **index.html/layout.html**: This is the main page of the website, where users can access the core functionalities of the platform. The page includes a header and five interactive containers, each leading to a different service:

  - **Polynomials.html**: This page allows users to input up to two polynomials. The platform then calculates and displays the roots of the first polynomial (including complex roots), the greatest common divisor (GCD), and the division of the first polynomial by the second.

  - **calculator.html**: A basic arithmetic and trigonometric calculator, where users can input mathematical expressions and obtain immediate results. This page supports various types of operations, from basic addition and subtraction to more complex trigonometric functions.

  - **functions.html/plots.html**: A page that lets users input a single-variable mathematical function. Once the function is entered, the platform generates the plot of the function, as well as its derivative and antiderivative. This feature works with complex functions, including Gaussian and Dirichlet functions, offering a more advanced tool for visualizing mathematical concepts.

  - **Series.html**: This page is designed to help users determine whether a given series converges or diverges. It allows users to input the infinite series (in function of n) and analyze its behavior.

  - **systems.html**: On this page, users can choose from one to four equations (with one as the default). They can then input multivariable equations, and the system will solve them, including cases where there are infinite solutions. This feature is especially useful for solving systems of equations.

All of these HTML files are connected to either external CSS files stored in the static folder or contain their own internal styles. The design of the website is structured to ensure a smooth user experience, with a clean and responsive layout that adapts to different screen sizes.
