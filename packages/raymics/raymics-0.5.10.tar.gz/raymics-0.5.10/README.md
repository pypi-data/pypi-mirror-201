# 提取Radiomics特征

## 1. 安装特征提取工具包


```python
!pip install --upgrade raymics
```

    Looking in indexes: https://pypi.org/simple, https://pypi.ngc.nvidia.com
    Requirement already satisfied: raymics in /Users/john/PycharmProjects/raymics-python/raymics (0.5.9)
    Requirement already satisfied: numpy in /Users/john/.virtualenvs/venv_py3.10/lib/python3.10/site-packages (from raymics) (1.22.4)
    Requirement already satisfied: pandas in /Users/john/.virtualenvs/venv_py3.10/lib/python3.10/site-packages (from raymics) (1.5.2)
    Requirement already satisfied: tqdm in /Users/john/.virtualenvs/venv_py3.10/lib/python3.10/site-packages (from raymics) (4.64.1)
    Requirement already satisfied: imageio in /Users/john/.virtualenvs/venv_py3.10/lib/python3.10/site-packages (from raymics) (2.24.0)
    Requirement already satisfied: av in /Users/john/.virtualenvs/venv_py3.10/lib/python3.10/site-packages (from raymics) (10.0.0)
    Requirement already satisfied: SimpleITK in /Users/john/.virtualenvs/venv_py3.10/lib/python3.10/site-packages (from raymics) (2.2.1)
    Requirement already satisfied: pyradiomics in /Users/john/.virtualenvs/venv_py3.10/lib/python3.10/site-packages (from raymics) (3.0.1)
    Requirement already satisfied: opencv-contrib-python in /Users/john/.virtualenvs/venv_py3.10/lib/python3.10/site-packages (from raymics) (4.7.0.68)
    Requirement already satisfied: dicom2nifti in /Users/john/.virtualenvs/venv_py3.10/lib/python3.10/site-packages (from raymics) (2.4.7)
    Requirement already satisfied: python-gdcm in /Users/john/.virtualenvs/venv_py3.10/lib/python3.10/site-packages (from dicom2nifti->raymics) (3.0.20)
    Requirement already satisfied: pydicom>=2.2.0 in /Users/john/.virtualenvs/venv_py3.10/lib/python3.10/site-packages (from dicom2nifti->raymics) (2.3.1)
    Requirement already satisfied: scipy in /Users/john/.virtualenvs/venv_py3.10/lib/python3.10/site-packages (from dicom2nifti->raymics) (1.10.0)
    Requirement already satisfied: nibabel in /Users/john/.virtualenvs/venv_py3.10/lib/python3.10/site-packages (from dicom2nifti->raymics) (4.0.2)
    Requirement already satisfied: pillow>=8.3.2 in /Users/john/.virtualenvs/venv_py3.10/lib/python3.10/site-packages (from imageio->raymics) (9.4.0)
    Requirement already satisfied: psutil in /Users/john/.virtualenvs/venv_py3.10/lib/python3.10/site-packages (from imageio->raymics) (5.9.4)
    Requirement already satisfied: imageio-ffmpeg in /Users/john/.virtualenvs/venv_py3.10/lib/python3.10/site-packages (from imageio->raymics) (0.4.8)
    Requirement already satisfied: python-dateutil>=2.8.1 in /Users/john/.virtualenvs/venv_py3.10/lib/python3.10/site-packages (from pandas->raymics) (2.8.2)
    Requirement already satisfied: pytz>=2020.1 in /Users/john/.virtualenvs/venv_py3.10/lib/python3.10/site-packages (from pandas->raymics) (2022.7)
    Requirement already satisfied: PyWavelets>=0.4.0 in /Users/john/.virtualenvs/venv_py3.10/lib/python3.10/site-packages (from pyradiomics->raymics) (1.4.1)
    Requirement already satisfied: pykwalify>=1.6.0 in /Users/john/.virtualenvs/venv_py3.10/lib/python3.10/site-packages (from pyradiomics->raymics) (1.8.0)
    Requirement already satisfied: six>=1.10.0 in /Users/john/.virtualenvs/venv_py3.10/lib/python3.10/site-packages (from pyradiomics->raymics) (1.16.0)
    Requirement already satisfied: ruamel.yaml>=0.16.0 in /Users/john/.virtualenvs/venv_py3.10/lib/python3.10/site-packages (from pykwalify>=1.6.0->pyradiomics->raymics) (0.17.21)
    Requirement already satisfied: docopt>=0.6.2 in /Users/john/.virtualenvs/venv_py3.10/lib/python3.10/site-packages (from pykwalify>=1.6.0->pyradiomics->raymics) (0.6.2)
    Requirement already satisfied: packaging>=17.0 in /Users/john/.virtualenvs/venv_py3.10/lib/python3.10/site-packages (from nibabel->dicom2nifti->raymics) (22.0)
    Requirement already satisfied: setuptools in /Users/john/.virtualenvs/venv_py3.10/lib/python3.10/site-packages (from nibabel->dicom2nifti->raymics) (67.6.0)
    Requirement already satisfied: ruamel.yaml.clib>=0.2.6 in /Users/john/.virtualenvs/venv_py3.10/lib/python3.10/site-packages (from ruamel.yaml>=0.16.0->pykwalify>=1.6.0->pyradiomics->raymics) (0.2.7)


## 2. 设定提取特征的选项
按照实际文件路径修改下面变量：


```python
from raymics.extract_radiomics_features import extract

dataset_dir = "./raw_data"                       # 原始数据文件夹，需要根据数据集文件夹的实际路径进行修改
result_dir = "./radiomics_feature_data"          # 用来放置特征数据文件夹，根据自己所希望的实际路径进行修改
config_path = "./radiomics.yaml"                 # radiomics配置文件，根据实际文件的路径进行修改

processes = 2
```

## 3. 执行特征提取


```python
extract(dataset_dir=dataset_dir, config=config_path, result_dir=result_dir, processes=processes);
```

    100%|███████████████████████████████████████████████████████████████████████████████████████| 2/2 [00:07<00:00,  3.84s/it]


注意，如果已经完成radiomics特征数据的提取，再次执行时会给出提示并终止执行，如下所示：


```python
extract(dataset_dir=dataset_dir, config=config_path, result_dir=result_dir, processes=processes);
```

    2023-04-04 10:17:46 [ERROR] raymics.log - The result dir './radiomics_feature_data' is not empty with files:
    - labels.csv
    - features.csv


## 4.  特征数据输出

在特征数据文件夹中会生成特征数据，如下所示(如不支持tree命令，可以直接到特征数据文件夹查看)：


```python
!tree ./radiomics_feature_data    # 使用实际特征文件夹路径替换
```

    [01;34m./radiomics_feature_data[0m
    ├── [00mfeatures.csv[0m
    └── [00mlabels.csv[0m
    
    0 directories, 2 files

