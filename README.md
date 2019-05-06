# Foodies Backend

This is the backend repository for Foodies, an app for Cornell AppDev's Hack Challenge, Spring 2019.
This site is current live at [foodies.leoliang.com](https://foodies.leoliang.com). Note that it is API only.

## Routes
### Get all foods: `GET /api/foods`
Returns a JSON representation of all foods like this:
```JSON
{
  "success": true,
  "data": [
    {
      "id": 1,
      "created_on": "May 4, 2019 1:20 am",
      "updated_on": "May 5, 2019 2:40 pm",
      "title": "Chinese Food",
      "location": "Gym",
      "location_detail": "Second Floor",
      "description": "Orange chicken available.",
      "start_time": "1:30 pm",
      "end_time": "2:40 pm",
      "date": "May 6, 2019",
      "tags": ["West", "meals"],
      "image": "<base64 of image data>"
    },
    {
      "id": 2,
      "created_on": "May 4, 2019 3:20 am",
      "updated_on": "May 5, 2019 4:40 pm",
      "title": "Mochi",
      "location": "Quad",
      "location_detail": "By the parking lot",
      "description": "Green tea and vanilla flavour.",
      "start_time": "2:10 pm",
      "end_time": "6:10 pm",
      "date": "May 8, 2019",
      "tags": ["North", "desserts"],
      "image": ""
    }
  ]
}
```

### Create a food: `POST /api/foods`
Takes a JSON body like this:
```JSON
{
  "title": "Burgers at English class",
  "location": "Tatkon",
  "location_detail": "Lobby",
  "description": "Vegan option available.",
  "start_time": "5:10 pm",
  "end_time": "7:10 pm",
  "date": "May 10, 2019",
  "tags": ["South", "meals"],
  "image": "<base64 of image data or empty string>"
}
```
Returns:
```JSON
{
  "success": true,
  "data": {
    "id": 2,
    "created_on": "May 4, 2019 3:20 am",
    "updated_on": "May 5, 2019 4:40 pm",
    "title": "Burgers at English class",
    "location": "Tatkon",
    "location_detail": "Lobby",
    "description": "Vegan option available.",
    "start_time": "5:10 pm",
    "end_time": "7:10 pm",
    "date": "May 10, 2019",
    "tags": ["South", "meals"],
    "image": "<base64 of image data or empty string>"
  }
}
```
or, in case of failure:
```JSON
{
  "success": false
}
```

## How to build/use
- Clone this repo.
- Make sure you have Python 3 installed with pip.
- Create and activate a virtualenv if you want (recommended).
- Run `pip3 install -r requirements.txt`.
- Run `python3 ./app.py`.
- The website is now live at `http://localhost:5000`.

## License
[MIT](LICENSE).

