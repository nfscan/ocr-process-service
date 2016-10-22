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

OS dependencies
```{Shell}
# for Yum on CentOS
yum install ImageMagick-c++-devel blas-devel lapack-devel python-devel
```

Cuneiform - Part 1

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

Cuneiform - Part 2

In case you've ```cuneiform``` installed under the ```/usr/local/bin``` directory then you may need make a few symbolic links in order to get that working.

```{Shell}
ln -s /usr/local/lib/libcuneiform.so.0 /usr/lib/libcuneiform.so.0
ln -s /usr/local/lib/librcorrkegl.so.0 /usr/lib/librcorrkegl.so.0
ln -s /usr/local/lib/librfrmt.so.0 /usr/lib/librfrmt.so.0
ln -s /usr/local/lib/librmarker.so.0 /usr/lib/librmarker.so.0
ln -s /usr/local/lib/librblock.so.0 /usr/lib/librblock.so.0
ln -s /usr/local/lib/librneg.so.0 /usr/lib/librneg.so.0
ln -s /usr/local/lib/librout.so.0 /usr/lib/librout.so.0
ln -s /usr/local/lib/libced.so.0 /usr/lib/libced.so.0
ln -s /usr/local/lib/librpic.so.0 /usr/lib/librpic.so.0
ln -s /usr/local/lib/librselstr.so.0 /usr/lib/librselstr.so.0
ln -s /usr/local/lib/librstuff.so.0 /usr/lib/librstuff.so.0
ln -s /usr/local/lib/librimage.so.0 /usr/lib/librimage.so.0
ln -s /usr/local/lib/librline.so.0 /usr/lib/librline.so.0
ln -s /usr/local/lib/librshelllines.so.0 /usr/lib/librshelllines.so.0
ln -s /usr/local/lib/librverline.so.0 /usr/lib/librverline.so.0
ln -s /usr/local/lib/libcimage.so.0 /usr/lib/libcimage.so.0
ln -s /usr/local/lib/libcfio.so.0 /usr/lib/libcfio.so.0
ln -s /usr/local/lib/libcpage.so.0 /usr/lib/libcpage.so.0
ln -s /usr/local/lib/liblns32.so.0 /usr/lib/liblns32.so.0
ln -s /usr/local/lib/librdib.so.0 /usr/lib/librdib.so.0
ln -s /usr/local/lib/libsmetric.so.0 /usr/lib/libsmetric.so.0
ln -s /usr/local/lib/libexc.so.0 /usr/lib/libexc.so.0
ln -s /usr/local/lib/libloc32.so.0 /usr/lib/libloc32.so.0
ln -s /usr/local/lib/librreccom.so.0 /usr/lib/librreccom.so.0
ln -s /usr/local/lib/librpstr.so.0 /usr/lib/librpstr.so.0
ln -s /usr/local/lib/librstr.so.0 /usr/lib/librstr.so.0
ln -s /usr/local/lib/libcline.so.0 /usr/lib/libcline.so.0
ln -s /usr/local/lib/librcutp.so.0 /usr/lib/librcutp.so.0
ln -s /usr/local/lib/libpass2.so.0 /usr/lib/libpass2.so.0
ln -s /usr/local/lib/librbal.so.0 /usr/lib/librbal.so.0
ln -s /usr/local/lib/librsadd.so.0 /usr/lib/librsadd.so.0
ln -s /usr/local/lib/libleo32.so.0 /usr/lib/libleo32.so.0
ln -s /usr/local/lib/libevn32.so.0 /usr/lib/libevn32.so.0
ln -s /usr/local/lib/libfon32.so.0 /usr/lib/libfon32.so.0
ln -s /usr/local/lib/libctb32.so.0 /usr/lib/libctb32.so.0
ln -s /usr/local/lib/libmsk32.so.0 /usr/lib/libmsk32.so.0
ln -s /usr/local/lib/libdif32.so.0 /usr/lib/libdif32.so.0
ln -s /usr/local/lib/libcpu32.so.0 /usr/lib/libcpu32.so.0
ln -s /usr/local/lib/libr3532.so.0 /usr/lib/libr3532.so.0
ln -s /usr/local/lib/libmmx32.so.0 /usr/lib/libmmx32.so.0
ln -s /usr/local/lib/librling.so.0 /usr/lib/librling.so.0
ln -s /usr/local/lib/librlings.so.0 /usr/lib/librlings.so.0
ln -s /usr/local/lib/libcstr.so.0 /usr/lib/libcstr.so.0
ln -s /usr/local/lib/libccom.so.0 /usr/lib/libccom.so.0
ln -s /usr/local/lib/libstd32.so.0 /usr/lib/libstd32.so.0
ln -s /usr/local/lib/libcfcompat.so.0 /usr/lib/libcfcompat.so.0
```

Finally
```{Shell}
git clone https://github.com/nfscan/ocr-process-service.git
cd ocr-process-service
pip install -r requirements.txt

sudo mv etc/init.d/ocr-process-service /etc/init.d
sudo chmod +x /etc/init.d/ocr-process-service
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

It's been noticed that cuneiform works more stable when running on 32 bits operational systems. We do believe that is no longer our hardware reality. So if you're a good C/C++ developer and want to port it to 64 bits OS feel free to do so :)

Make ocr-process-service to process a image locally instead of waiting it through a AWS SQS queue.

## Contributing 

You're encouraged to contribute to nfscan. Fork the code from https://github.com/nfscan/ocr-process-service and submit pull requests.

Make sure you're following the [contributing guidelines](https://github.com/nfscan/ocr-process-service/blob/master/CONTRIBUTING.md) for this project.
