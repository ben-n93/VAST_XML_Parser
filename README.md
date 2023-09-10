# VAST XML Parser

A Video Ad Serving Template (VAST) 2.0/3.0 XML parser that extracts **Creative** and **MediaFile** element metadata and presents this information in an application built on the PyQt5 GUI framework:

<img width="1107" alt="Screen Shot 2022-02-16 at 4 03 41 pm" src="https://user-images.githubusercontent.com/84557025/154199660-a992261a-3c47-4074-b5e2-74faf778b30e.png">

*VAST is a Video Ad Serving Template for structuring ad tags that serve ads to video players. Using an XML schema, VAST transfers important metadata about an ad from the ad server to a video player.* Read more [here](https://www.iab.com/guidelines/vast/).

## Inspiration

Examining a raw VAST tag response is timely, particlarly when wanting to test the creative/media files, so I created this application to make it quicker and easier to read MediaFile metadata and to copy the creative files' URLs.

## How it works

Parses the VAST XML tree for the **MediaFile** element and populates the application table with both the **MediaFile** content/file and attributes/values.

Also populates application fields with **Creative** element's ID and AdID attribute values (if present), as well as highest and lowest bitrate values.

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

Launch program:
```python
$ python3 vast_xml_parser.py
```

## License

Distributed under the Apache-2.0 License. See LICENSE.txt for more information.
