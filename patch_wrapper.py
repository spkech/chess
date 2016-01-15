from mock import patch


class PatchWrapper(object):

    """ PatchWrapper is a wrapper providing higher level patch_module and patch_object methods for 'mock' module's
        patch and patch.object methods."""

    @staticmethod
    def patch_module(testcase_object, module_to_patch, **kwargs):
        """ Patches a given module in the scope of the function it was called from and returns the mocked module.
        **kwargs is the dictionary containing the key-value arguments passed to the original patch method."""

        patcher = patch(module_to_patch, **kwargs)
        mock_module = patcher.start()
        testcase_object.addCleanup(patcher.stop)
        return mock_module

    @staticmethod
    def patch_object(testcase_object, class_of_method_to_patch, method_to_patch, **kwargs):
        """ Patches a given method of an object of a given class in the scope of the function it was called from and
        returns the mocked method.
        **kwargs is the dictionary containing the key-value arguments passed to the original patch method."""

        patcher = patch.object(class_of_method_to_patch, method_to_patch, **kwargs)
        mock_method = patcher.start()
        testcase_object.addCleanup(patcher.stop)
        return mock_method
