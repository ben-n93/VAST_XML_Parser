# VAST XML Parser

A Video Ad Serving Template (VAST) 2.0/3.0 XML parser that extracts MediaFile metadata and presents this information in an application built on the PyQt5 GUI framework:

<img width="1107" alt="Screen Shot 2022-02-15 at 6 07 49 pm" src="https://user-images.githubusercontent.com/84557025/154014268-2b5972f9-cdc7-481b-9e5a-e09e53806e7a.png">

*VAST is a Video Ad Serving Template for structuring ad tags that serve ads to video players. Using an XML schema, VAST transfers important metadata about an ad from the ad server to a video player.* Read more [here](https://www.iab.com/guidelines/vast/).

## How it works

Parses the VAST XML tree for the **MediaFile** element and populates the application table with both the **MediaFile** content/file and attributes/values.

If there is no MediaFile element then the table does not populate.

## Sample tag

A Single InLine Linear tag sourced from Google's [IMA sample tags](https://developers.google.com/interactive-media-ads/docs/sdks/html5/client-side/tags) was used for the above screenshot/example.

## Installation

Download the source files or clone the code to your virtual enviroment:

``` python
$ git clone https://github.com/ben-n93/VAST_XML_Parser.git
```
Navigate into the parent directory and install the required packages:

```python
$ cd VAST_XML_Parser
$ pip3 install -r requirements.txt
```

Execute script:
```python
$ python3 vast_xml_parser.py
```
## Planned features

This is still a work in progress. A VAST tag can return different responses/MediaFiles and, other than examining the MediaFiles themselves, the only way to know is to look at the Creative element ID attribute (if present) and I plan on capturing/presenting this Creative ID in a future iteration of the application.

## License

Distributed under the Apache-2.0 License. See LICENSE.txt for more information.
