## Objective

Create a simple mobile web application for showing demo ads. Take measures to ensure quality and maintainability and briefly document the application, explaining the decisions you made.

## Description

The application consists of two parts:

  - the client, which is a simple HTML5 web application and
  - the web service, which serves the client and allows CRUD operations on the data.

The client should be a single-page HTML5 web application that runs on mobile devices. Once the user opens the demo client in their mobile device's browser, they are presented with a list of folders. Tapping a folder shows them the list of ads that are in that folder. Tapping one of the ads should open the ad URL in a new window.

Ads, in this case, are just arbitrary URLs. Their implementation is not within the scope of this assignment.

## Requirements

  - The client uses the web service to read data. You don't have to build any other clients that may also support create, update and delete operations, but those operations should nevertheless be supported by the web service. Have in mind that multiple clients can use the web service at the same time.

  - You will obviously have to use browser technologies to build the client but, other than that, there are no other limitations, so you are free to use any language, library, preprocessor, build system, etc. that you choose.

  - For the web service, the choice of technology is absolutely up to you: any programming language, framework, data storage, etc. can be used.

  - Authentication is not mandatory.

  - The choice of architectures, communication protocols and formats is up to you.

  - You should be able to derive the data model yourself from the description.

  - The quality and maintainability of the application (both the client and the web service) needs to be ensured to some extent with automatic tests.

  - Finally, the application should be documented, explaining the architectural, technological and other decision you made.
