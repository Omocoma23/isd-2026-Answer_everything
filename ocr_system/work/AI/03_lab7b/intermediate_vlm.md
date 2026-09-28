\documentclass[1200.0x1754.0]{standalone}
\usepackage{amsmath,amsfonts,graphicx,color}
\usepackage{tikz-cd}

\usetikzlibrary {positioning}
\tikzset {
    &gt;={Latex[length=3pt]},
    myangleектор/.append style={
        angle eccentricity = 1.5,
        angle radius = 2mm,
        angle position = -90:
    },
    myangle vector/.append style={
        angle eccentricity = 1.5,
        angle radius = 2mm,
        angle position = 90:
    },
    mynode/.append style={draw, fill=white, inner sep=3pt},
    tcancel/.append style={draw=#1!85},
}

\begin{document}
    
    \begin{table}[h]
        \caption{รายละเอียดหลักสูตรวท.บ.(สาขาวิชาเทคโนโลยีปัญญาประดิษฐ์) คณะเทคโนโลยีสารสนเทศ สจล.} 
        \label{tab:1}
        \begin{tr}
            <td>รหัสวิชา</td><td>ชื่อวิชา</td><td>หน่วยกิต (บรรยาย-ปฏิบัติ-ศึกษาด้วยตนเอง)</td>
        </tr>
        \foreach\x[count=\i] in{06046415, การประมวลผลสัญญาณ 3(3-0-6), SIGNAL PROCESSING,
            06046416, การเรียนรู้เชิงลึกสำหรับคอมพิวเตอร์วิทัศน์ 3 (3-0-6), DEEP LEARNING FOR COMPUTER VISION,
            06046417, การประมวลผลภาพ 3(3-0-6), IMAGE PROCESSING,
            06046418, การระบุตำแหน่งและการสร้างแผนที่ของหุ่นยนต์ 3 (3-0-6), ROBOT LOCALIZATION AND MAPPING,
            06046419, การเรียนรู้แบบเสริมกำลัง 3(3-0-6), REINFORCEMENT LEARNING,
            06046420, ระบบให้คำแนะนำอัจฉริยะ 3 (3-0-6), INTELLIGENT RECOMMENDATION SYSTEMS,
            06046421, การประมวลผลภาษาธรรมชาติขั้นสูง 3(3-0-6), ADVANCED NATURAL LANGUAGE PROCESSING,
            06046422, จริยธรรมด้านปัญญาประดิษฐ์ 3 (3-0-6), ARTIFICIAL INTELLIGENCE ETHICS,
            06046423, การออกแบบบริการด้านปัญญาประดิษฐ์ 3(3-0-6), ARTIFICIAL INTELLIGENCE SERVICE DESIGN,
            06046424, ตรรกะและการแทนความรู้ 3 (3-0-6), LOGIC AND KNOWLEDGE REPRESENTATION,
            06046425, โมเดลแบบกำเนิด 3(3-0-6), GENERATIVE MODEL,
            06046430, หัวข้อคัดสรรด้านปัญญาประดิษฐ์ 1 3 (3-0-6), SELECTED TOPICS IN ARTIFICIAL INTELLIGENCE 1,
            06046431, หัวข้อคัดสรรด้านปัญญาประดิษฐ์ 2 3(3-0-6), SELECTED TOPICS IN ARTIFICIAL INTELLIGENCE 2,
            06046432, หัวข้อคัดสรรด้านปัญญาประดิษฐ์ 3 3 (3-0-6), SELECTED TOPICS IN ARTIFICIAL INTELLIGENCE 3,
            06046433, หัวข้อคัดสรรด้านปัญญาประดิษฐ์ 4 3(3-0-6), SELECTED TOPICS IN ARTIFICIAL INTELLIGENCE 4,
            06046434, หัวข้อคัดสรรด้านปัญญาประดิษฐ์ 5 3 (3-0-6), SELECTED TOPICS IN ARTIFICIAL INTELLIGENCE 5,
            06046435, หัวข้อคัดสรรด้านปัญญาประดิษฐ์ 6 3(3-0-6), SELECTED TOPICS IN ARTIFICIAL INTELLIGENCE 6}
        \end{tr}
    </table>
    
\end{document}

---

\documentclass[1230.8x1754.2]{article}
\usepackage{amsmath,amsfonts,graphicx,latexsym,color}
\usepackage{tikz}%&lt;&lt;&lt;
\tikzset{
    mycircle/.style={
        fill=red!6,
        draw=black,
        inner sep=1pt
      },
    myrectangle/.style={
        fill=white,
        draw=black,
        inner sep=2pt
      },
    myrectangle2/.style={
        fill=white,
        draw=black,
        inner sep=0.5pt
      },
    myrectangle3/.style={
        fill=white,
        draw=black,
        inner sep=1pt
      },
    myrectangle4/.style={
        fill=red!6,
        draw=black,
        inner sep=2pt
      },
    myrectangle5/.style={
        fill=red!6,
        draw=black,
        inner sep=0.5pt
      },
    myrectangle6/.style={
        fill=white,
        draw=black,
        inner sep=1pt
      },
    myrectangle7/.style={
        fill=white,
        draw=black,
        inner sep=2pt
      },
    myrectangle8/.style={
        fill=red!6,
        draw=black,
        inner sep=0.5pt
      }
  }

\usepackage{tikz}
\usetikzlibrary {positioning}

\begin{document}

\begin{table}[h]
\caption{รายละเอียดหลักสูตรกลุ่มวิชาโครงงานและสัมมนา (2018-2019) สาขาวิชาวิศวกรรมศาสตร์อุตสาหกรรมคอมพิวเตอร์ คณะเทคโนโลยีสารสนเทศ สจล.)}
\begin{tr><td>รหัสวิชา</td><td>ชื่อวิชา</td><td>หน่วยกิต (บรรยาย-ปฏิบัติ-ศึกษาด้วยตนเอง)</td></tr>
<tr><td>06046440</td><td>วิชาสัมมนาปัญญาประดิษฐ์<br/>SEMINAR IN ARTIFICIAL INTELLIGENCE</td><td>3 (2-2-5)</td></tr>
<tr><td>06046441</td><td>โครงงานเทคโนโลยีปัญญาประดิษฐ์ 1<br/>PROJECT IN ARTIFICIAL INTELLIGENCE TECHNOLOGY 1</td><td>3 (0-9-0)</td></tr>
<tr><td>06046442</td><td>โครงงานเทคโนโลยีปัญญาประดิษฐ์ 2<br/>PROJECT IN ARTIFICIAL INTELLIGENCE TECHNOLOGY 2</td><td>3 (0-9-0)</td></tr>
<tr><td>06046443</td><td>สหกิจศึกษาทางเทคโนโลยีปัญญาประดิษฐ์<br/>COOPERATIVE EDUCATION IN ARTIFICIAL<br/>INTELLIGENCE TECHNOLOGY หรือ<br/>OVERSEA COOPERERATIVE EDUCATION IN ARTIFICIAL<br/>INTELLIGENCE TECHNOLOGY</td><td>6 (0-45-0)</td></tr>
<tr><td>06046444</td><td>สหกิจศึกษาต่างประเทศทางเทคโนโลยีปัญญาประดิษฐ์<br/>OVERSEA COOPERERATIVE EDUCATION IN ARTIFICIAL<br/>INTELLIGENCE TECHNOLOGY หรือ<br/>COOPERATIVE EDUCATION IN ARTIFICIAL<br/>INTELLIGENCE TECHNOLOGY</td><td>6 (0-45-0)</td></tr></table>

นักศึกษาเลือกลงทะเบียนเรียนวิชาสหกิจศึกษาหรือสหกิจศึกษาต่างประเทศทางเทคโนโลยีปัญญาประดิษฐ์วิชาใดวิชาหนึ่ง จำนวนรวม 6 หน่วยกิต กำหนดระยะเวลาในการทำสหกิจศึกษาเป็นเวลาอย่างน้อย 16 สัปดาห์หรือ 1 ภาคการศึกษา

ค. หมวดวิชาเลือกเสรี
นักศึกษาสามารถเลือกเรียนในรายวิชาที่เปิดสอนในสถาบันเทคโนโลยีพระจอมเกล้าเจ้าคุณทหารลาดกระบัง จำนวนไม่น้อยกว่า 6 หน่วยกิต

ความหมายของรหัสประจำรายวิชา
รหัสวิชาที่ใช้กำหนดให้เป็นตัวเลขและตัวอักษร 8 หลัก (จากมติสภาวิชาการ ครั้งที่ 11/2553)
<table><tr><td>รหัสตัวที่</td><td></td><td>ได้แก่ เลข</td><td>หมายถึง</td><td>คณะเทคโนโลยีสารสนเทศ</td></tr><tr><td>1, 2</td><td></td><td>06</td><td></td><td></td></tr><tr><td>3,4</td><td></td><td>04</td><td>หมายถึง</td><td>สาขาวิชาเทคโนโลยีปัญญาประดิษฐ์</td></tr><tr><td></td><td>ได้แก่ เลข</td><td>06</td><td>หมายถึง</td><td>วิชาเรียนรวม</td></tr><tr><td>5</td><td></td><td>6</td><td>หมายถึง</td><td>ระดับปริญญาตรี</td></tr><tr><td>6, 7, 8</td><td></td><td>หมายถึง</td><td colspan="2">ลำดับที่ของรายวิชา</td></tr></table>

วท.บ.(สาขาวิชาวิศวกรรมศาสตร์อุตสาหกรรมคอมพิวเตอร์) คณะเทคโนโลยีสารสนเทศ สจล.

\end{table}
\end{document}

---

\documentclass[120mm]{a4paper}
\usepackage{amsmath,amsfonts,graphicx,latexsym,color}
\usepackage{tikz}%&lt;&lt;&lt;
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&

---

\documentclass[120mm]{a4paper}
\usepackage{amsmath,amsfonts,graphicx,color}
\usepackage{tikz-cd}

\usetikzlibrary {positioning}

\begin{document}

\pagestyle{fancy}
\centering

<table><tr><td>รหัสวิชา</td><td>ชื่อวิชา</td><td>หน่วยกิต<br/>(บรรยาย-ปฏิบัติ-ศึกษาด้วยตนเอง)</td></tr><tr><td>06066300</td><td>แนวคิดระบบฐานข้อมูล<br/>DATABASE SYSTEM CONCEPTS</td><td>3 (2-2-5)</td></tr><tr><td>06046405</td><td>การเรียนรู้ของเครื่องเชิงความน่าจะเป็น<br/>PROBABILISTIC MACHINE LEARNING</td><td>3 (3-0-6)</td></tr><tr><td>06046406</td><td>พื้นฐานการเรียนรู้เชิงลึก<br/>FUNDAMENTALS OF DEEP LEARNING</td><td>3 (3-0-6)</td></tr><tr><td>06046409</td><td>คอมพิวเตอร์วิทัศน์เบื้องต้น<br/>INTRODUCTION TO COMPUTER VISION</td><td>3 (3-0-6)</td></tr><tr><td>06046413</td><td>ปัญญาประดิษฐ์และอินเทอร์เน็ตประสานสรรพสิ่ง<br/>ARTIFICIAL INTELLIGENCE AND INTERNET OF THING</td><td>3 (3-0-6)</td></tr><tr><td rowspan="2">90641009</td><td>ทักษะการสื่อสารภาษาอังกฤษระหว่างวัฒนธรรม 1<br/>INTERCULTURAL COMMUNICATION SKILLS IN ENGLISH 1</td><td>3 (3-0-6)</td></tr><tr><td></td><td></td></tr><tr><td colspan="2">รวม</td><td>18</td></tr></table>

\begin{table}
    \centering
    \caption{ปีที่ 2 ภาคการศึกษาที่ 2}
    \label{tab:2nd_semesters_2023-24}
    \begin{array}{|c|c|c|}
        \hline 
        \textbf{รหัสวิชา} &amp; \textbf{ชื่อวิชา} &amp; \textbf{หน่วยกิต<br/>(บรรยาย-ปฏิบัติ-ศึกษาด้วยตนเอง)} \\
        06046407 &amp; พื้นฐานวิทยาการข้อมูล<br/>FUNDAMENTALS OF DATA SCIENCE &amp; 3 (3-0-6)\\
        06046408 &amp; การแสดงข้อมูลด้วยแผนภาพ<br/>DATA VISUALIZATION &amp; 3 (2-2-5)\\
        06046410 &amp; การประมวลผลภาษาธรรมชาติเบื้องต้น<br/>INTRODUCTION TO NATURAL LANGUAGE PROCESSING &amp; 3 (3-0-6)\\
        06046412 &amp; การเพิ่มประสิทธิภาพโครงข่ายประสาทเทียม<br/>NEURAL NETWORK OPTIMIZATION &amp; 3 (3-0-6)\\
        06046411 &amp; การวิเคราะห์และเพิ่มประสิทธิภาพเครือข่าย<br/>NETWORK ANALYSIS AND OPTIMIZATION &amp; 3 (3-0-6)\\
        90641010 &amp; ทักษะการสื่อสารภาษาอังกฤษระหว่างวัฒนธรรม 2<br/>INTERCULTURAL COMMUNICATION SKILLS IN ENGLISH 2 &amp; 3 (3-0-6)\\
        90641005 &amp; โครงงานกลุ่ม 2<br/>TEAM-PROJECT 2 &amp; 1 (0-2-1)\\
    \end{array}
\end{table}

วท.บ.(สาขาวิชาเทคโนโลยีปัญญาประดิษฐ์) คณะเทคโนโลยีสารสนเทศ สจล.

\begin{figure}[center]
    \includegraphics[width=0.85]{image_url_of_seal}
</figure>

รายละเอียดหลักสูตร

---

\documentclass[1200.8x1754.2]{standalone}
\usepackage{amsmath,amsfonts,graphicx,latexsym,color}
\usepackage{tikz-cd}

\usetikzlibrary {positioning}

\begin{document}

\begin{table}[c] 
    \caption[ ]{ปีที่ 3 ภาคการศึกษาที่ 1}
    \label[ ]{p1-3a}
    \begin{tr} 
        <td>รหัสวิชา</td><td>ชื่อวิชา</td><td>หน่วยกิต (บรรยาย-ปฏิบัติ-ศึกษาด้วยตนเอง)</td>
    </tr> 
    \foreach\x[count=\i] in{06046415, การประมวลผลสัญญาณ SIGNAL PROCESSING, 3(3-0-6), 06046414, การประมวลผลภาษาธรรมชาติด้วยการเรียนรู้อย่างเชิงลึก NATURAL LANGUAGE PROCESSING WITH DEEP LEARNING, 3 (3-0-6), 90642012, กระบวนการคิดเชิงออกแบบ DESIGN THINKING, 3(3-0-6), 060464xx, วิชาเลือกเทคโนโลยีปัญญาประดิษฐ์เฉพาะทาง ELECTIVE IN ARTIFICIAL INTELLIGENCE SPECIALIZATION, 6 (3-0-6), 06046440, วิชาสัมมนาปัญญาประดิษฐ์ SEMINAR IN ARTIFICIAL INTELLIGENCE, 3(2-2-5), รวม, 18}
    \i
        \end{tr} 
\end{table}

\begin{table}[c] 
    \caption[ ]{ปีที่ 3 ภาคการศึกษาที่ 2}
    \label[ ]{p1-3b}
    \begin{tr} 
        <td>รหัสวิชา</td><td>ชื่อวิชา</td><td>หน่วยกิต (บรรยาย-ปฏิบัติ-ศึกษาด้วยตนเอง)</td>
    </tr> 
    \foreach\x[count=\i] in{060464xx, วิชาเลือกเทคโนโลยีปัญญาประดิษฐ์เฉพาะทาง ELECTIVE IN ARTIFICIAL INTELLIGENCE SPECIALIZATION, 6 (3-0-6), 06046441, โครงงานเทคโนโลยีปัญญาประดิษฐ์ 1 PROJECT IN ARTIFICIAL INTELLIGENCE TECHNOLOGY 1, 3(0-9-0), 90641006, โครงงานกลุ่ม 3 TEAM-PROJECT 3, 1 (0-2-1), xxxxxxxxx, วิชาเลือกเสรี 1 FREE ELECTIVE COURSE 1, 3(x-x-x), รวม, 13}
    \i
        \end{tr} 
\end{table}

วท.บ.(สาขาวิชาเทคโนโลยีปัญญาประดิษฐ์) คณะเทคโนโลยีสารสนเทศ สจล.
\end{document}

---

Extract all text from the image.

Instructions:
- Only return the clean Markdown.
- Do not include any explanation or extra text.
- You must include all information on the page.

Formatting Rules:
- Tables: Render tables using <table>...</table> in clean HTML format.
- Equations: Render equations using LaTeX syntax with inline ($...$) and block ($$...$$).
- Images/Charts/Diagrams: Wrap any clearly defined visual areas (e.g. charts, diagrams, pictures) in:

<figure>
Describe the image’s main elements (people, objects, text), note any contextual clues (place, event, culture), mention visible text and its meaning, provide deeper analysis when relevant (especially for financial charts, graphs, or documents), comment on style or architecture if relevant, then give a concise overall summary. Describe in Thai.
</figure>


- Page Numbers: Wrap page numbers in <page_number>...</page_number> (e.g., <page_number>14</page_number>).
- Checkboxes: Use ☐ for unchecked and ☑ for checked boxes.
