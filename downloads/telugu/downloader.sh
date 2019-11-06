echo Downloading files...

axel http://web-language-models.s3-website-us-east-1.amazonaws.com/ngrams/te/raw/te.2012.raw.xz
axel http://web-language-models.s3-website-us-east-1.amazonaws.com/ngrams/te/raw/te.2013_20.raw.xz
axel http://web-language-models.s3-website-us-east-1.amazonaws.com/ngrams/te/raw/te.2013_48.raw.xz
axel http://web-language-models.s3-website-us-east-1.amazonaws.com/ngrams/te/raw/te.2014_15.raw.xz
axel http://web-language-models.s3-website-us-east-1.amazonaws.com/ngrams/te/raw/te.2014_23.raw.xz
axel http://web-language-models.s3-website-us-east-1.amazonaws.com/ngrams/te/raw/te.2014_35.raw.xz
axel http://web-language-models.s3-website-us-east-1.amazonaws.com/ngrams/te/raw/te.2014_41.raw.xz
axel http://web-language-models.s3-website-us-east-1.amazonaws.com/ngrams/te/raw/te.2014_42.raw.xz
axel http://web-language-models.s3-website-us-east-1.amazonaws.com/ngrams/te/raw/te.2014_49.raw.xz
axel http://web-language-models.s3-website-us-east-1.amazonaws.com/ngrams/te/raw/te.2014_52.raw.xz
axel http://web-language-models.s3-website-us-east-1.amazonaws.com/ngrams/te/raw/te.2015_06.raw.xz
axel http://web-language-models.s3-website-us-east-1.amazonaws.com/ngrams/te/raw/te.2015_11.raw.xz
axel http://web-language-models.s3-website-us-east-1.amazonaws.com/ngrams/te/raw/te.2015_14.raw.xz
axel http://web-language-models.s3-website-us-east-1.amazonaws.com/ngrams/te/raw/te.2015_18.raw.xz
axel http://web-language-models.s3-website-us-east-1.amazonaws.com/ngrams/te/raw/te.2015_22.raw.xz
axel http://web-language-models.s3-website-us-east-1.amazonaws.com/ngrams/te/raw/te.2015_27.raw.xz
axel http://web-language-models.s3-website-us-east-1.amazonaws.com/ngrams/te/raw/te.2015_32.raw.xz
axel http://web-language-models.s3-website-us-east-1.amazonaws.com/ngrams/te/raw/te.2015_35.raw.xz
axel http://web-language-models.s3-website-us-east-1.amazonaws.com/ngrams/te/raw/te.2015_40.raw.xz
axel http://web-language-models.s3-website-us-east-1.amazonaws.com/ngrams/te/raw/te.2015_48.raw.xz
axel http://web-language-models.s3-website-us-east-1.amazonaws.com/ngrams/te/raw/te.2016_30.raw.xz
axel http://web-language-models.s3-website-us-east-1.amazonaws.com/ngrams/te/raw/te.2016_50.raw.xz
axel http://web-language-models.s3-website-us-east-1.amazonaws.com/ngrams/te/raw/te.2017_17.raw.xz

echo Extracting files...
unxz -kv *.xz
# rm *.xz
