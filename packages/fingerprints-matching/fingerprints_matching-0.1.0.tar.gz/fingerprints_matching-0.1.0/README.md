Fingerprint Matching Algorithm
---------------------------------------------

This is a Python implementation of the fingerprint minutiae matching algorithm which will be used in the comparison of two fingerprints and calculate the similarity between them using the match score.

If Match Score is greater than 0.9, then the two fingerprints are more likely to be from the same person and if Match Score is less than 0.9, then it can be concluded that the two fingerprints are not from the same person.

Fingerprint Module Installation
-------------------------------

The recommended way to install the `fingerprints_matching` module is to simply use `pip`:

```console
$ pip install fingerprints_matching
```
Fingerprint Matching officially supports Python >= 3.0.

How to use fingerprint?
-----------------------
```pycon
>>> from fingerprints_matching import FingerprintsMatching
>>> match_score = FingerprintsMatching.fingerprints_matching("image1.png", "image2.png")
```