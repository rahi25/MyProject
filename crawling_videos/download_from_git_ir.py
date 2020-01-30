#!/home/rahi/anaconda3/envs/myenv/bin/python3.7
"""
    Program: Downloading video from git.ir
    Author: Ehsan Rahnama
    Copyright: 2019
"""

import requests
from bs4 import BeautifulSoup
import re
import urllib
import os
import time
import argparse


class bcolors:
    HEADER = '\033[35m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    OkCAYAN = '\033[96m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def download_video_link(url):
    """

    :param url: address to download videos
    :return: all links video --> type list
    """
    page = requests.get(url)
    soup = BeautifulSoup(page.content)
    links = soup.find_all("a")

    video_links = []
    for link in links:
        link_ = link.get('href')
        if re.findall(r"(https://)\w.*mp4", link_):
            video_links.append(link_)
    
    return video_links


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--url", required=True, help="This is url for download video from <git.ir>")
    parser.add_argument("-o", "--output", help="Store videos in directory",
                        default=os.environ.get('output', './Download'))

    args = parser.parse_args()

    PATH = args.output
    if os.path.exists(PATH):
        print(f"\nThis '{PATH}' directory exist!!!")
    else:
        os.mkdir(PATH)

    # Open file to write missing info of downloading file
    lost = open(f"{PATH}/lose_file.txt", "w")

    url = args.url

    videos = download_video_link(url)

    print("\n")
    print("=" * 50)
    print(f"There are {bcolors.HEADER}{bcolors.BOLD}{len(videos)}{bcolors.ENDC} videos file ready to download")
    print("=" * 50)
    enter = input("Please enter yes or no\n")

    while True:
        if enter == "y" or enter == "yes":
            print(
                bcolors.OKBLUE + bcolors.BOLD + "\n------------- Start Downloading Videos -------------\n" + bcolors.ENDC)
            time.sleep(5)

            ss = time.time()
            ii = 1
            lost_download = 0
            for video in videos:
                name = video.split("/")[-1]
                print(f"{bcolors.BOLD}Start download video ---> {name}{bcolors.ENDC}")
                try:
                    urllib.request.urlretrieve(video, PATH + "/" + name)
                except Exception as e:
                    lost.write(f"Error-->{e}\tlostfile-->{name}\n")
                    lost_download += 1
                    print(f"{bcolors.FAIL}{e}{bcolors.ENDC}")

                print(f"{bcolors.OKGREEN}Finish {ii}/{len(videos)}{bcolors.ENDC}")

                ii += 1
            ee = time.time()
            print(bcolors.UNDERLINE + "\nDownloading Finished\n" + bcolors.ENDC)
            print(f"{bcolors.WARNING}Lost Downloded --> {lost_download}{bcolors.ENDC}\n")

            print(f"{bcolors.OkCAYAN}Downloading time --> {(ee - ss) // 60} Minute{bcolors.ENDC}")
            break

        elif enter == "n" or enter == "no":
            print(bcolors.OkCAYAN + bcolors.BOLD + "GOOD BYE !!!!" + bcolors.ENDC)
            break
        else:
            print(bcolors.FAIL + "Uhhhhh... you enter incorrectly!" + bcolors.ENDC)
            enter = input("Please enter yes or no\n")
