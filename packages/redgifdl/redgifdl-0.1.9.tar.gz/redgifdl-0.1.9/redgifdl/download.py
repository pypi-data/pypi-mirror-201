import sys
import traceback
import requests
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
log = logging.getLogger(__name__)

def url_file(redgifs_url, filename):
    """
    It takes a RedGifs URL and a filename, and downloads the video to the filename
    
    :param redgifs_url: The URL of the RedGifs video you want to download
    :param filename: The name of the file to save the video as
    :return: The URL of the HD video.
    """
    sys.stdout.reconfigure(encoding='utf-8')
    API_URL_REDGIFS = 'https://api.redgifs.com/v1/gifs/'
    try:
        log.info("redgifs_url = {}".format(redgifs_url))

        #Get RedGifs video ID
        redgifs_ID = redgifs_url.split('/watch/', 1)
        redgifs_ID = redgifs_ID[1].replace("/", "")
        log.info("redgifs_ID = {}".format(redgifs_ID))
        
        sess = requests.Session()
        
        request = sess.get(API_URL_REDGIFS + redgifs_ID)
        
        if request is None:
            return
        else:

            def write_stream(hd_url, filename):
                with sess.get(hd_url, stream=True) as r:
                    with open(filename, 'wb') as f:
                        for chunk in r.iter_content(chunk_size=8192): 
                            f.write(chunk)

            rawData = request.json()
            #Get HD video url
            try:
                hd_video_url = rawData['gif']['urls']['hd']
                log.debug("URL = {}".format(hd_video_url))
                write_stream(hd_video_url, filename)
                


                return hd_video_url
            except:
                try:
                    # gfyItem
                    hd_video_url = rawData['gfyItem']['content_urls']['mp4']['url']
                    log.debug("URL = {}".format(hd_video_url))
                    write_stream(hd_video_url, filename)
                    return hd_video_url
                
                except:
                    hd_video_url = rawData['gfyItem']['content_urls']['mobile']['url']
                    log.debug("URL = {}".format(hd_video_url))
                    write_stream(hd_video_url, filename)
                    return hd_video_url
                

    except Exception:
        traceback.print_exc()
        return
