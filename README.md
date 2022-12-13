# modern-optics-hw

2022年秋季学期-中山大学电子与信息工程学院-现代光学大作业-光源光谱与色域特性计算

## 问题：

A. 查阅技术资料，得到某种发光器件技术（如OLED、QLED、LED）中RGB三基色的典型光谱，绘制类似于如下左图的光谱功率分布，图必须完全由程序生成，不含导入的位图.

B. 由上述RGB三基色的光谱计算其CIE1931 XYZ色品坐标，并在色品图上绘制类似于如下右图的色域，计算色域大小——以NTSC色域为基准，给出类似于“NTSC 90%“的定量结论（难度系数75%）.

在完成A和B基础上，以下两题选择其一：

C. 查阅CIE2006色彩匹配函数，重新执行色域计算，与上述基于CIE1931的结果同时绘制于色品图上。考虑不同光源技术的不同色域表现，探讨色域对两种色彩匹配函数差异的影响（难度系数95%）.

D. 在上述RGB光源的基础上，加入第四个基色（如黄色），假定第四个基色的光谱宽度、分布等与RGB类似，重新计算此时的色域，分析第四个基色为何种颜色时色域提升最大（难度系数120%）.

![1667878868245](./assets/1667878868245.png)

左图：光谱功率分布；右图：色品图与色域

## 参考资料

### 程序 (深度借鉴！)

* colour -- [colour-science/colour: Colour Science for Python (github.com)](https://github.com/colour-science/colour)

  ```shell
  # 安装
  git clone git@github.com:colour-science/colour.git
  python setup.py build && python setup.py install 
  # pip方式
  pip install colour-science
  # conda方式
  conda install -c conda-forge colour-science
  ```
* luox [luox-app/luox: Code base for the luox platform (github.com)](https://github.com/luox-app/luox)
* [Illuminant Data (uwaterloo.ca)](http://www.npsg.uwaterloo.ca/data/illuminant.php)
* [Spectra Code (sfasu.edu)](http://www.physics.sfasu.edu/astro/color/spectra.html)波长转颜色 [Exploring the Visible Spectrum in Python - CodeDromeCodeDrome](https://www.codedrome.com/exploring-the-visible-spectrum-in-python/) [python - Matplotlib - color under curve based on spectral color - Stack Overflow](https://stackoverflow.com/questions/44959955/matplotlib-color-under-curve-based-on-spectral-color) [Color Science (midnightkite.com)](http://www.midnightkite.com/color.html) [Spectra Code (sfasu.edu)](http://www.physics.sfasu.edu/astro/color/spectra.html)

### 理论

* [CIE1931标准色度系统_QinLanXin的博客-CSDN博客_cie1931标准色度系统](https://blog.csdn.net/QinLanXin/article/details/88884669)
* [色域马蹄图是怎么来的？——CIE 1931 XYZ色彩空间详解 - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/137639368)

### 数据来源：

keyword: `site:cie.co.at STANDARD ILLUMINANT csv`

* [LSPDD | Light Spectral Power Distribution Database](https://lspdd.org/app/en/lamps?page=1)
* [Data Tables | CIE](https://cie.co.at/data-tables)
* [colord/data/illuminant at main · hughsie/colord (github.com)](https://github.com/hughsie/colord/tree/main/data/illuminant)
* colour [colour/colour/colorimetry/datasets at develop · colour-science/colour (github.com)](https://github.com/colour-science/colour/tree/develop/colour/colorimetry/datasets)

三刺激值

* RGB [cie.15.2004.pdf (archive.org)](https://ia902802.us.archive.org/23/items/gov.law.cie.15.2004/cie.15.2004.pdf) [色差仪的三原色单位量和三次激值 - 深圳市三恩时科技有限公司 (3nh.com)](http://www.3nh.com/news/739.html)
* XYZ [Law.Resource.Org](https://law.resource.org/pub/us/cfr/ibr/003/) colour\colorimetry\datasets\cmfs.py

[ciexyz29082000.pdf (docs-hoffmann.de)](http://docs-hoffmann.de/ciexyz29082000.pdf)

LED

* [Spectral Power Distribution of LED (color.support)](http://color.support/ledspd.html)
* https://www.google.com.hk/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwi_5v65_fP7AhUXaN4KHZKBAlMQFnoECBUQAQ&url=https%3A%2F%2Fsites.psu.edu%2Fllab%2Ffiles%2F2020%2F02%2FCQS9.0.3-Win-5nm.xls&usg=AOvVaw0rtuRZxRA6YFNfHxrx51nf [Downloads | Lighting Lab (psu.edu)](https://sites.psu.edu/llab/downloads/)
* [C I E L a b . X Y Z • Специализированные профили для цветоделения](https://cielab.xyz/profiles/#WIG) https://www.google.com.hk/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwjM-P_f__P7AhVI0GEKHYniB_8QFnoECBMQAQ&url=https%3A%2F%2Fcielab.xyz%2Fpdf%2FNIST%2520CQS%2520simulation%25207.4.xls&usg=AOvVaw0KvUCgnUkk7YWtHDCBCKbK
* [Index of /406 (auld.me.uk)](http://bramley.auld.me.uk/406/) http://bramley.auld.me.uk/406/Calculating%20CRI-CAM02UCS-v2.xls
* [Spectral Calculator - Illuminating Engineering Society (ies.org)](https://www.ies.org/standards/standards-toolbox/tm-30-spectral-calculator/)

[Statement (auniontech.com)](https://www.auniontech.com/ueditor/file/20171225/1514172625322631.pdf) 三基色图介绍

* [Spectral Calculator - Illuminating Engineering Society (ies.org)](https://www.ies.org/standards/standards-toolbox/tm-30-spectral-calculator/)
* [LED Spectrum Simulator | Waveform Lighting](https://www.waveformlighting.com/led-spectrum-simulator/)

[如何在OpticStudio中使用Osram LED光源数据 – 中文帮助 (zemax.com)](https://support.zemax.com/hc/zh-cn/articles/1500005486661)

[Opto Semiconductors | OSRAM](https://www.osram.com/apps/downloadcenter/os/?path=%2Fos-files%2FOptical+Simulation%2FLED%2F)

[CVRL main](http://www.cvrl.org/) [Colour matching functions (cvrl.org)](http://www.cvrl.org/cmfs.htm)
