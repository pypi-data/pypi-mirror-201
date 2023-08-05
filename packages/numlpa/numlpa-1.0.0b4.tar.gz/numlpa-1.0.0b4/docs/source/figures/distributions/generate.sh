source ../../../../setup.sh

mkdir samples

numlpa draw samples/dipoles -n 1 dipoles
numlpa draw samples/images -n 1 images
numlpa draw samples/wilkens -n 1 wilkens

rm -r dipoles
rm -r images
rm -r wilkens

numlpa export samples/dipoles dipoles basic --pairs
numlpa export samples/images images basic --pairs
numlpa export samples/wilkens wilkens basic

rm -r samples
