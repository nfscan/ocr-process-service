# ocr-process-service

[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/nfscan/ocr-process-service/master/LICENSE)

ocr-process-service is open-source software available to retrieve meaningful values from Brazilian receipts

## Setting up environment

**Dependencies**

Tesseract
```
# Follow these instructions
https://code.google.com/p/tesseract-ocr/wiki/Compiling

Obs.: Make sure you have tesseract accessible under the /usr/bin/ 
A symbolic link will do the trick ;)
```

Cuneiform

```{Shell}
git clone https://github.com/PauloMigAlmeida/cuneiform.git
cd cuneiform
mkdir builddir
cd builddir
cmake -DCMAKE_BUILD_TYPE=release ..
make
make install

Obs.: Make sure you have cuneiform accessible under the /usr/bin/ 
A symbolic link will do the trick ;)
```

ImageMagick-devel
```
libmagickwand-dev for APT on Debian/Ubuntu
imagemagick for MacPorts/Homebrew on Mac
ImageMagick-devel for Yum on CentOS
```

Finally
```{Shell}
git clone https://github.com/nfscan/ocr-process-service.git
cd ocr-process-service
pip install -r requirements.txt

sudo mv etc/init.d/ocr-process-service /etc/init.d
sudo mkdir -p /etc/ocr-process-service
sudo mv etc/ocr-process-service/* /etc/ocr-process-service/
python script.py
```

##Config

ocr-process-service works on top of boto to access AWS services under the hoods. It makes us to have two configuration files. 

* **Boto config**

    Take a look a [this](http://boto.readthedocs.org/en/latest/boto_config_tut.html)

* **ocr-process-service.cfg**

    If you have followed [this tutorial](https://github.com/nfscan/nfscan/wiki/Develpment-environment---%5BPortuguese%5D) then it's likely that your config file will look like this:

    ```
    [aws_account]
    default_region = sa-east-1
    
    [aws_sqs]
    queue_name_in = DES-NFSCAN-OCR-PROCESS-IN
    queue_name_out = DES-NFSCAN-OCR-PROCESS-OUT
    
    [aws_s3]
    bucket_name = TheBucketNameYouHaveCreated
    ```

## TODO

It's been noticed that cuneiform works more stable when running on 32 bits operational systems. We do believe that this is no longer our hardware reality. So if you're a good C/C++ developer and want to port it to 64 bits OS feel free to do so :)

Make ocr-process-service to process a image locally instead of waiting it through a AWS SQS queue.

## Contributing 

You're encouraged to contribute to nfscan. Fork the code from https://github.com/nfscan/ocr-process-service and submit pull requests.

Make sure you're following the [contributing guidelines](https://github.com/nfscan/ocr-process-service/blob/master/CONTRIBUTING.md) for this project.
