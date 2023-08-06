# vripper

A Python implementation of VRipper. See the list of supported websites below.

## Installation

```bash
# Python 3.6+
pip install vripper
```

## Usage

```python
from vripper import download_thread

if should_disable_logging:
    logging.getLogger("vripper").setLevel(logging.CRITICAL)

thread_url = "https://..."
dest = os.path.join(".", "vripper")

download_thread(thread_url, dest, **options)
```

### Options

Not in any particular order

|Name|Type|Default Value|Description|
|---|---|---|---|
|`mode`|vripper.enum<br>.downloadmode<br>.DownloadMode|`FIRST_POST_ONLY`|Determines which post(s) within the thread to download.|
|`output_format`|vripper.enum<br>.outputformat<br>.OutputFormat|None|The desired output format. Currently supported: zip|
|`download_threadpool_size`|`int`|5|The number of concurrent threads for the download. The minimum allowed value is 1.|
|`processing_pool_size`|`int`|0|The number of concurrent processes for the pre/post-processing. Set it to 0 to disable multiprocessing.|
|`max_filecount`|`int`|None|The max number of files (images) allowed in a post. If the number of files exceeds the given value, the module skip a subset of images. Ex. Download every 3rd image.|
|`min_dimension`|`int` (pixels)|0|The min dimension allowed for an image. Images whose dimensions are smaller than this value will be deleted.|
|`max_dimension`|`int` (pixels)|None|The max dimension allowed for an image. If the downloaded image exceeds the given value, the image will be resized.|
|`max_filesize`|`int` (bytes)|None|Any files larger than this threshold will be deleted.|
|`min_filesize`|`int` (bytes)|None|Any files smaller than this threshold will be deleted.|
|`acceptable_filesize`|`int` (bytes)|None|Any files smaller than this threshold will not be considered for resize/compression. Expressed in bytes.|
|`min_hitrate`|`float`|.85|A minimum percentage of files in a post required to be downloaded and processed successfully.|
|`download_connect_timeout`|`float` (seconds)|1.0|The time it takes to abort the connection with the image host.|
|`download_read_timeout`|`float` (seconds)|10.0|The time it takes to abort the read with the image host.|
|`compression_quality`|`int`|65|JPEG compression quality -- more info [here](https://pillow.readthedocs.io/en/5.1.x/handbook/image-file-formats.html). Set it to 0 to disable the compression. The value cannot be 0 if `max_dimension` has been specified.|
|`processing_priority`|vripper.enum<br>.processingpriority<br>.ProcessingPriority|None|Determines the course of action, given two conflicting options. Example TBD|


### Exceptions

For each image subject to download, there is a potential for the download to be considered unsuccessful. To name a few reasons:

* Temporary network issues;
* The host going offline temporarily or permanently;
* The image was deleted by the uploader;
* The downloaded file is corrupted; or
* The downloaded file size is too small/big based on the user-specified threshold.

In the end, if the total number of successfully downloaded images does not meet `min_hitrae`, the module will throw one of the following exceptions:

Note: If the post has more images than the value specified in `max_filecount`, not all images will be subject to download. The skipped images will not be considered for the `min_hitrate` calculation.

|Name|Calculation Time|Description|
|---|---|---|
|`PermissionError`|Pre-download|Raised when the requested thread is private.|
|`UnsupportedHostError`|Pre-download|Raised when the number of images hosted by unsupported websites is too high.|
|`DeprecatedHostError`|Pre-download|Raised when the number of images hosted by deprecated websites is too high.|
|`ImagePermanentlyUnavailableError`|Post-download|Raised when the number of deleted images is too high.|
|`InsufficientFileCountError`|Final|Raised when the number of resulting files in a post is too low.|
