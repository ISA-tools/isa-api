import unittest

from isatools.net.mtbls2isa_ds_assay_definitions import *


class MyTestCase(unittest.TestCase):

    def test_load_terms_from_owl(self):

        cl_names, class_list, file_checksum = load_terms_from_mtbls_owl(MTBLS_CV_OWL)
        self.assertEqual(file_checksum, "6aca7b750af9e5f9cfe7744c51084217b0664e2fd5ef163afabed44efe74ee98")
        self.assertEqual(cl_names[0], "instruments")
        self.assertEqual(str(class_list[0].identifier), "http://www.ebi.ac.uk/metabolights/ontology/MTBLS_000283")


    # def test_parse_mtbls_assay_def(self):
    #     reference_assays = []
    #     isa_ds_assays = parse_mtbls_assay_def(file,
    #                                           class_names,
    #                                           associated_subclasses,
    #                                           "6aca7b750af9e5f9cfe7744c51084217b0664e2fd5ef163afabed44efe74ee98")
    #     self.assertEqual(isa_ds_assays, reference_assays)


    # def test_make_parameter_values(self):
    #
    #     test_param_setup = build_params_slim.make_param_values(["chromatography instrument", "column"], [] )
    #     self.assertEqual(test_param_setup, reference_data)