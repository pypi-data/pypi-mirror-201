from fingerprints_matching import minutiae_matching


class FingerprintsMatching:
    def __init__(self):
        pass

    @staticmethod
    def fingerprints_matching(image_path1: str, image_path2: str):
        # Extract the minutiae from the two images
        minutiae1 = minutiae_matching.extract_minutiae(image_path1)
        minutiae2 = minutiae_matching.extract_minutiae(image_path2)

        # Perform minutiae matching
        match_result = minutiae_matching.match(minutiae1, minutiae2)

        # Return the matching score
        return match_result
