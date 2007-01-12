#!/usr/bin/env python

## Program:   VMTK
## Module:    $RCSfile: vmtkimagereader.py,v $
## Language:  Python
## Date:      $Date: 2006/05/22 08:33:12 $
## Version:   $Revision: 1.16 $

##   Copyright (c) Luca Antiga, David Steinman. All rights reserved.
##   See LICENCE file for details.

##      This software is distributed WITHOUT ANY WARRANTY; without even 
##      the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR 
##      PURPOSE.  See the above copyright notices for more information.

import vtk
import vtkvmtk
import sys

import pypes

vmtkimagereader = 'vmtkImageReader'

class vmtkImageReader(pypes.pypeScript):

    def __init__(self):

        pypes.pypeScript.__init__(self)
        
        self.Format = ''
        self.GuessFormat = 1
        self.UseITKIO = 1
        self.InputFileName = ''
        self.InputFilePrefix = ''
        self.InputFilePattern = ''
        self.InputDirectoryName = ''
        self.Image = 0
        self.Output = 0

        self.DataExtent = [-1, -1, -1, -1, -1, -1]
        self.DataSpacing = [1.0, 1.0, 1.0]
        self.DataOrigin = [0.0, 0.0, 0.0]
        self.DataByteOrder = 'littleendian'
        self.DataScalarType = 'float'
        self.HeaderSize = 0
        self.FileDimensionality = 3
        self.Flip = [0, 0, 0]
        self.AutoOrientDICOMImage = 1

        self.SetScriptName('vmtkimagereader')
        self.SetScriptDoc('read an image and stores it in a vtkImageData object')
        self.SetInputMembers([
            ['Format','f','str',1,'file format (vtkxml, vtk, dicom, raw, meta image, tiff, png)'],
            ['GuessFormat','guessformat','int',1,'guess file format from extension'],
            ['UseITKIO','useitk','int',1,'use ITKIO mechanism'],
            ['InputFileName','i','str',1,'input file name (deprecated: use -ifile)'],
            ['InputFileName','ifile','str',1,'input file name'],
            ['InputFilePrefix','prefix','str',1,'input file prefix (e.g. foo_)'],
            ['InputFilePattern','pattern','str',1,'input file pattern (e.g. %s%04d.png)'],
            ['InputDirectoryName','d','str',1,'input directory name - dicom only'],
            ['DataExtent','extent','int',6,'3D extent of the image - raw and png'],
            ['HeaderSize','headersize','int',1,'size of the image header - raw only'],
            ['DataSpacing','spacing','float',3,'spacing of the image - raw, tiff, png'],
            ['DataOrigin','origin','float',3,'origin of the image - raw, tiff, png'],
            ['DataByteOrder','byteorder','str',1,'byte ordering (littleendian, bigendian) - raw only'],
            ['DataScalarType','scalartype','str',1,'scalar type (float, double, int, short, ushort, uchar) - raw only'],
            ['FileDimensionality','filedimensionality','int',1,'dimensionality of the file to read - raw only'],
            ['Flip','flip','int',3,'toggle flipping of the corresponding axis'],
            ['AutoOrientDICOMImage','autoorientdicom','int',1,'flip a dicom stack in order to have a left-to-right, posterio-to-anterior, inferior-to-superior image; this is based on the \"image orientation (patient)\" field in the dicom header']
            ])
        self.SetOutputMembers([
            ['Image','o','vtkImageData',1,'the output image','vmtkimagewriter']
            ])

    def ReadVTKXMLImageFile(self):
        if (self.InputFileName == ''):
            self.PrintError('Error: no InputFileName.')
        self.PrintLog('Reading VTK XML image file.')
        reader = vtk.vtkXMLImageDataReader()
        reader.SetFileName(self.InputFileName)
        reader.Update()
        self.Image = reader.GetOutput()

    def ReadVTKImageFile(self):
        if (self.InputFileName == ''):
            self.PrintError('Error: no InputFileName.')
        self.PrintLog('Reading VTK image file.')
        reader = vtk.vtkStructuredPointsReader()
        reader.SetFileName(self.InputFileName)
        reader.Update()
        self.Image = reader.GetOutput()

    def ReadRawImageFile(self):
        if (self.InputFileName == '') & (self.InputFilePrefix == ''):
            self.PrintError('Error: no InputFileName or InputFilePrefix.')
        self.PrintLog('Reading RAW image file.')
        reader = vtk.vtkImageReader()
        if self.InputFileName != '':
            reader.SetFileName(self.InputFileName)
        else:
            reader.SetFilePrefix(self.InputFilePrefix)
            if self.InputFilePattern != '':
                reader.SetFilePattern(self.InputFilePattern)
            else:
                reader.SetFilePattern("%s%04d.png")
        reader.SetFileDimensionality(self.FileDimensionality)
        if self.DataByteOrder == 'littleendian':
            reader.SetDataByteOrderToLittleEndian()
        elif self.DataByteOrder == 'bigendian':
            reader.SetDataByteOrderToBigEndian()
        reader.SetDataExtent(self.DataExtent)
        reader.SetDataSpacing(self.DataSpacing)
        reader.SetDataOrigin(self.DataOrigin)
      	reader.SetHeaderSize(self.HeaderSize)
      	if self.DataScalarType == 'float':
      	    reader.SetDataScalarTypeToFloat()
       	elif self.DataScalarType == 'double':
      	    reader.SetDataScalarTypeToDouble()
       	elif self.DataScalarType == 'int':
      	    reader.SetDataScalarTypeToInt()
       	elif self.DataScalarType == 'short':
      	    reader.SetDataScalarTypeToShort()
       	elif self.DataScalarType == 'ushort':
      	    reader.SetDataScalarTypeToUnsignedShort()
      	elif self.DataScalarType == 'uchar':
      	    reader.SetDataScalarTypeToUnsignedChar()
        reader.Update()
        self.Image = reader.GetOutput()

    def ReadMetaImageFile(self):
        if (self.InputFileName == ''):
            self.PrintError('Error: no InputFileName.')
        self.PrintLog('Reading meta image file.')
        reader = vtk.vtkMetaImageReader()
        reader.SetFileName(self.InputFileName)
        reader.Update()
        self.Image = reader.GetOutput()

    def ReadTIFFImageFile(self):
        if (self.InputFileName == '') & (self.InputFilePrefix == ''):
            self.PrintError('Error: no InputFileName or InputFilePrefix.')
        self.PrintLog('Reading TIFF image file.')
        reader = vtk.vtkTIFFReader()
        if self.InputFileName != '':
            reader.SetFileName(self.InputFileName)
        else:
            reader.SetFilePrefix(self.InputFilePrefix)
            if self.InputFilePattern != '':
                reader.SetFilePattern(self.InputFilePattern)
            else:
                reader.SetFilePattern("%s%04d.png")
            reader.SetDataExtent(self.DataExtent)
            reader.SetDataSpacing(self.DataSpacing)
            reader.SetDataOrigin(self.DataOrigin)
        reader.Update()
        self.Image = reader.GetOutput()

    def ReadPNGImageFile(self):
        if (self.InputFileName == '') & (self.InputFilePrefix == ''):
            self.PrintError('Error: no InputFileName or InputFilePrefix.')
        self.PrintLog('Reading PNG image file.')
        reader = vtk.vtkPNGReader()
        if self.InputFileName != '':
            reader.SetFileName(self.InputFileName)
        else:
            reader.SetFilePrefix(self.InputFilePrefix)
            if self.InputFilePattern != '':
                reader.SetFilePattern(self.InputFilePattern)
            else:
                reader.SetFilePattern("%s%04d.png")
            reader.SetDataExtent(self.DataExtent)
            reader.SetDataSpacing(self.DataSpacing)
            reader.SetDataOrigin(self.DataOrigin)
        reader.Update()
        self.Image = reader.GetOutput()

    def ReadDICOMFile(self):
        if (self.InputFileName == ''):
            self.PrintError('Error: no InputFileName.')
        self.PrintLog('Reading DICOM file.')
        reader = vtkvmtk.vtkvmtkDICOMImageReader()
        reader.SetFileName(self.InputFileName)
        reader.SetAutoOrientImage(self.AutoOrientDICOMImage)
        reader.Update()
        self.Image = reader.GetOutput()

    def ReadDICOMDirectory(self):
        if (self.InputDirectoryName == ''):
            self.PrintError('Error: no InputDirectoryName.')
        self.PrintLog('Reading DICOM directory.')
        reader = vtkvmtk.vtkvmtkDICOMImageReader()
        reader.SetDirectoryName(self.InputDirectoryName)
        reader.SetAutoOrientImage(self.AutoOrientDICOMImage)
        reader.Update()
        self.Image = reader.GetOutput()

    def ReadITKIO(self):
        if self.InputFileName == '':
            self.PrintError('Error: no InputFileName.')
        reader = vtkvmtk.vtkITKArchetypeImageSeriesScalarReader()
        reader.SetArchetype(self.InputFileName)
        reader.SetOutputScalarTypeToNative()
        reader.SetDesiredCoordinateOrientationToNative()
#        reader.SetDesiredCoordinateOrientationToAxial()
        reader.SetUseNativeOriginOn()
        reader.Update()
        self.Image = vtk.vtkImageData()
        self.Image.DeepCopy(reader.GetOutput())

    def Execute(self):

        extensionFormats = {'vti':'vtkxml', 
                            'vtkxml':'vtkxml', 
                            'vtk':'vtk',
                            'dcm':'dicom',
                            'raw':'raw',
                            'mhd':'meta',
                            'mha':'meta',
                            'tif':'tiff',
                            'png':'png'}

        if self.GuessFormat and self.InputFileName and not self.Format:
            import os.path
            extension = os.path.splitext(self.InputFileName)[1]
            if extension:
                extension = extension[1:]
                if extension in extensionFormats.keys():
                    self.Format = extensionFormats[extension]

        if self.UseITKIO and self.Format not in ['vtkxml']:
            self.ReadITKIO()    
        else:
            if self.Format == 'vtkxml':
                self.ReadVTKXMLImageFile()
            elif self.Format == 'vtk':
                self.ReadVTKImageFile()
            elif self.Format == 'dicom':
                if self.InputDirectoryName != '':
                    self.ReadDICOMDirectory()
                else:
                    self.ReadDICOMFile()
            elif self.Format == 'raw':
                self.ReadRawImageFile()
            elif self.Format == 'meta':
                self.ReadMetaImageFile()
            elif self.Format == 'png':
                self.ReadPNGImageFile()
            elif self.Format == 'tiff':
                self.ReadTIFFImageFile()
            else:
                self.PrintError('Error: unsupported format '+ self.Format + '.')

        if (self.Flip[0] == 1) | (self.Flip[1] == 1) | (self.Flip[2] == 1):
            temp0 = self.Image
            if self.Flip[0] == 1:
                flipFilter = vtk.vtkImageFlip()
                flipFilter.SetInput(self.Image)
                flipFilter.SetFilteredAxis(0)
                flipFilter.Update()
                temp0 = flipFilter.GetOutput()
            temp1 = temp0
            if self.Flip[1] == 1:
                flipFilter = vtk.vtkImageFlip()
                flipFilter.SetInput(temp0)
                flipFilter.SetFilteredAxis(1)
                flipFilter.Update()
                temp1 = flipFilter.GetOutput()
            temp2 = temp1
            if self.Flip[2] == 1:
                flipFilter = vtk.vtkImageFlip()
                flipFilter.SetInput(temp1)
                flipFilter.SetFilteredAxis(2)
                flipFilter.Update()
                temp2 = flipFilter.GetOutput()
            self.Image = temp2

        if self.Image.GetSource():
            self.Image.GetSource().UnRegisterAllOutputs()

        self.Output = self.Image

if __name__=='__main__':
    main = pypes.pypeMain()
    main.Arguments = sys.argv
    main.Execute()

