# -*- coding: utf-8 -*-
"""
Created on Sat Mar 25 15:34:15 2023

@author: Hedi
"""

import wx


def to_html_saveas(main_frame,project):

    with wx.FileDialog(main_frame, "Save csv file", wildcard="csv files (*.html)|*.html",
                        style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:

        if fileDialog.ShowModal() == wx.ID_CANCEL:
            return     # the user changed their mind

        # save the current contents in the file
        pathname = fileDialog.GetPath()
        try:
               project.pinch.to_html(pathname,main_frame.html_template_filename,main_frame.html_css_template_filename)
        except IOError:
            wx.LogError("Cannot save current data in file '%s'." % pathname)