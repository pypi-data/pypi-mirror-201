# LastFMTools

This is repo of pythons scripts, i created over the past year or so that utilize
lastfm scrobbling feature, and public lastfm api to create visualizations of user listening history.
you can try using them at: [LastFMTools.app](https://sea-lion-app-rlgof.ondigitalocean.app)

### Tools:

##### GIF-Mosaic

![alt text](https://github.com/Heroesluk/azure2/blob/add_other/static/examples/movie2readme.gif)

##### Bubble-Chart

![alt text](https://github.com/Heroesluk/azure2/blob/add_other/static/examples/example2readme.png)

##### Color-Chart

![alt text](https://github.com/Heroesluk/azure2/blob/add_other/static/examples/colormosaicreadme.jpg)

## Okay but what is LastFM in the first place?

Last.fm is a music streaming and recommendation service that allows users to create personalized music profiles,
discover new music, and connect with other music enthusiasts.

The scrobbling feature of Last.fm tracks the music you listen to on various platforms and records it on your profile.
This data is used to analyze your music taste and listening history.

## Can i test those scripts without having LastFM account? 

Sure, there's *random* feature for every tool, that lets you use script without providing your
LastFM nickname, providing you with image created from profile of random lastfm user

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install lastfmtools.

```bash
pip install lastfmtools
```

## Example usage:

```python
import LastFMTools

# creates bubble chart consisting of 50 most listened to albums, for user MyNickname, and 
# saves it as bubble.png
bubble_chart = BubbleChart("album", 50, "bubble.png", "MyNickname")

# creates gif of mosaic pictures, thay displays 25 favorite albums for each month,
# from november 2022, onwards, and saves it as File.gif  
gif_mosaic = GifMosaic("01-11-2022", "month", 5, "File.gif", "MyNickName")

# create mosaic that displays 16 album covers that 
# have biggest percentage of yellow, or similar colors in it, according to [CIE94](https://en.wikipedia.org/wiki/Color_difference#CIE94)
color_mosaic = ColorMosaic(COLOR.YELLOW, 4, "Yellow.png")

```

## Contribution

If you think there's anything to improve in those scripts,
then feel free to create issues and pull-requests,

## License

[MIT](https://choosealicense.com/licenses/mit/)
