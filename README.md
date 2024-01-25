<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/nepomuk3000/pyMyDatec2Mqtt">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">pyMyDatec2Mqtt</h3>

  <p align="center">
    An awesome Gateway between MyDatec double-flow mechanical ventilation Modbus and MQTT !
    <br />
    <a href="https://github.com/nepomuk3000/pyMyDatec2Mqtt"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/nepomuk3000/pyMyDatec2Mqtt">View Demo</a>
    ·
    <a href="https://github.com/nepomuk3000/pyMyDatec2Mqtt/issues">Report Bug</a>
    ·
    <a href="https://github.com/nepomuk3000/pyMyDatec2Mqtt/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#todo">TODO</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screen Shot][product-screenshot]](https://example.com)

The features provided with the communication card of my MyDatec double-flow mechanical ventilation was very poor so I created this software
* to get informations from the equipment Modbus to provide them to any home automation system thru MQTT protocol
* to control main functionnalities of the double-flow mechanical ventilation thru MQTT protocol too

To do so, I used a RS485 to WiFi server (Elfin EW11 bought on Aliexpress wor less than 15 €)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

The project does not needs any third party libraries.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

...

### Prerequisites

Only runs on Linux OS

### Installation

...

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

The start script (./scripts/start.sh) starts the daemon in nohup mode

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## TODO
[] Récupérer l'étalonnage ou la température étalonnée de la sonde de la zone de jour depuis le bus. Actuellement -2.3 en dur dans le code 
[] Implémenter une remontée d'erreur en MQTT
[] Implementer le protocole MQTT homeassistant
[] Permettre le paramétrage du sereur TCP
[] Documenter la configuration de Elfin EW11
[] Ameliorer la prise en compte de la consigne (conflit entre serveur mqtt et écran myDatec)
[] Commander la gestion de l'humidité et des COV /!\ Contrairement à ce qui est indiqué dans le document ne semblent pas remonter par 16493,16494
[] Lire et remonter les consommations /!\ Contrairement à ce qui est indiqué dans le document ne semblent pas remonter par 9049,9051,9053,9055

See the [open issues](https://github.com/nepomuk3000/pyMyDatec2Mqtt/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Project Link: [https://github.com/nepomuk3000/pyMyDatec2Mqtt](https://github.com/nepomuk3000/pyMyDatec2Mqtt)

<p align="right">(<a href="#readme-top">back to top</a>)</p>
