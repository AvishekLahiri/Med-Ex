# Med-Ex (Software Engineering Project)

<p align="center">
  <img src="img/img1.png">
</p>
<p align="center">
  <img src="img/img2.png">
</p>

For the coursework of 2018 BS-MS and 2020 MSc.-Ph.D Computer Science, IACS Kolkata. The project team comprises of:  

    I. Avishek Lahiri, 2020/SMCS/004
    II. Sarthak Das, 2018/UG/026
    III. Shubhajit Roy, 2020/SMCS/003

## The Problem

Read the following description of a software system as demanded by a prospective customer (wholesaler of medicines.)

The to-be-developed software has a number of retailers, a number of distributors under its jurisdiction. Every retailer/distributor may collect medicines from the wholesaler on prior requisition either on credit or on payment. Each retailer/distributor has to maintain a security deposit (customized) with the wholesaler. Needless to say is that the wholesaler has to maintain individual accounts of each and every retailer/distributor. The underlying requirements need to be fulfilled.

1. A retailer/distributor can collect medicines on credit of an amount not exceeding its security deposit. An automatic alarm is generated the moment 50% of its security deposit gets exhausted by the use of credit based collection. A copy of the alert will also be diverted automatically to the wholesaler so that it may follow up the matter with the concerned retailer/distributor.

2. As the administrator the wholesaler may alter the 50% credit flexibility level as stated above depending upon the consistent track record of the retailer/distributor.

3. The status of all retailers/distributors may be observed by the wholesaler whenever it is felt. A retailer may observe the status of itself only and not of any other retailer/distributor nor of the wholesaler.

On the basis of the above, prepare a Software Requirement Specification (SRS) with detailing of all its components. On the basis of the developed SRS, provide a Data Flow Diagram (DFD) to the level of detailing as may be necessary.

## The Solution

The SRS can be found in the root directory. The consequent data flow diagram for the same is as follows, and has also been added as an appendix to the SRS.

<p align="center">
  <img src="img/Data Flow Diagram.png">
</p>

## Source Code

A source code for the software prototype can be found in the /src/ directory. To run the software, one can run the following command in terminal.

```shell
git clone https://github.com/dassarthak18/Med-Ex.git
cd Med-Ex/src
sudo chmod u+x run_tool.sh
./run_tool.sh
```
