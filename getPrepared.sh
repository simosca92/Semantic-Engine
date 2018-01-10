#!/bin/bash  

if ! dpkg -s pv > /dev/null; then 
	echo "Installing PV..."	
	sudo apt-get install pv
fi

git clone https://github.com/tonikelope/megadown.git
cd megadown
chmod +x megadown
./megadown 'https://mega.nz/#!r1NHAYSL!fPUyKkC13DCNSTeO4ZpokywmxtkXo5IsmL_7LnQWCdI' -o./model1.zip
./megadown 'https://mega.nz/#!D91W2aBC!WSML2_C0rGP7jeRRRIa-ELziuSvVFJrG_a5_s8Sw1Rw' -o./model2.zip
mv  model1.zip ../models
mv  model2.zip ../models
cd ..
rm -R megadown
cd models
unzip model1.zip
rm model1.zip
unzip model2.zip
rm model2.zip
