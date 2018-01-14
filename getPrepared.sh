#!/bin/bash  

if ! dpkg -s pv > /dev/null; then 
	echo "Installing PV..."	
	sudo apt-get install pv
fi

git clone https://github.com/tonikelope/megadown.git
cd megadown
chmod +x megadown

# MODELS
./megadown 'https://mega.nz/#!r1NHAYSL!fPUyKkC13DCNSTeO4ZpokywmxtkXo5IsmL_7LnQWCdI' -o./model1.zip
./megadown 'https://mega.nz/#!D91W2aBC!WSML2_C0rGP7jeRRRIa-ELziuSvVFJrG_a5_s8Sw1Rw' -o./model2.zip
./megadown 'https://mega.nz/#!qxsU1bZB!mSSwG6LNSfas9exhSaZi5HUnFPbbmBzs-dyi1384IF0' -o./model3.zip

# OBJ
./megadown 'https://mega.nz/#!Sw8nXIDY!NRj0Tsv3cDQ6c6Vdrf5LO1NYe_G0iuhksqntuisOv2k' -o./obj.zip

# CORPUS FASTSENT
./megadown 'https://mega.nz/#!at1mXbCJ!gdeFko8o0VQEY0nVfq_A4TePfXmjq9xmofDBNMxMkjA' -o./corpus.zip

mv  model1.zip ../models
mv  model2.zip ../models
mv  model3.zip ../models
mv  obj.zip ../models
mv  corpus.zip ../corpus

cd ..
rm -R megadown
cd models
unzip model1.zip
rm model1.zip
unzip model2.zip
rm model2.zip
unzip model3.zip
rm model3.zip
unzip obj.zip
rm obj.zip

cd ../corpus
unzip corpus.zip
rm corpus.zip
