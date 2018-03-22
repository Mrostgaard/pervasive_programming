# Assignment 1 - Functional Requirements - Deadline April 12th
What is the architecture - How do you work towards that

* Measurement of temperature in the lake/canal outside our building
* Storage and presentation/visualization

What is the architecture - How do you work towards that;
Gateway, Testing etc.

## Technology choices

###### Hardware
We will be using LoPy as our knowledge and experience is greater here than other choices. LoPy can be used together with MicroPython, which we also have some experience in.
For energy we will probably use a mobile battery - watchout for minus degrees

###### Sensors
We will be using the waterproof temperature sensor which can be found here: https://www.sparkfun.com/products/11050.

###### Platform
We will be using a server at ITU. Currently we are thinking about centralized solutions such as Amazon IoT or Digital Ocean.

###### Network
Wi-Fi would be the easiest, but also most expensive regarding energy consumption.
LoRa might be a better choice, if the university has an active hub. More research needed.

###### Visual Presentation
Graph diagram such as Grafana - ChartJS

###### Error Handling
How will we be handling errors - on device and server vice

###### Storage
Database such as Influx or MySQL

###### Data
float, integer etc?

Lora if low - wifi if large
Timestamping - goes wrong, really bad, where/how what are the differences.
batch or single measurement
Physical security, theft etc.
