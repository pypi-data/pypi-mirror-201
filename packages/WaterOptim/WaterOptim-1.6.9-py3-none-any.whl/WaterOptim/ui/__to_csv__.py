# -*- coding: utf-8 -*-
"""
Created on Sat Mar 25 09:19:43 2023

@author: Hedi
"""

import wx


def to_csv_saveas(main_frame,project):

    with wx.FileDialog(main_frame, "Save csv file", wildcard="csv files (*.csv)|*.csv",
                        style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:

        if fileDialog.ShowModal() == wx.ID_CANCEL:
            return     # the user changed their mind

        # save the current contents in the file
        pathname = fileDialog.GetPath()
        try:
               project.pinch.to_csv(pathname)
        except IOError:
            wx.LogError("Cannot save current data in file '%s'." % pathname)