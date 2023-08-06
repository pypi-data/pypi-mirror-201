<!-- Filename:      README.md -->
<!-- Author:        Jonathan Delgado -->
<!-- Description:   GitHub README -->

<!-- Header -->
<h2 align="center">Typing Filter</h2>
  <p align="center">
    Simple CLI for a typing filter to provide choices to a user and let them type in phrases which filters possible options.
    <br />
    <br />
    Status: <em>in progress</em>
    <!-- Documentation link -->
    <!-- ·<a href="https://stochastic-thermodynamics-in-python.readthedocs.io/en/latest/"><strong>
        Documentation
    </strong></a> -->
    <!-- Notion Roadmap link -->
    ·<a href="https://otanan.notion.site/Typing-Filter-bf53e901c68b4e11b231d4d4578d32f2"><strong>
        Notion Roadmap »
    </strong></a>
  </p>
</div>


<!-- Project Demo -->
https://user-images.githubusercontent.com/6320907/230550634-3ac6b92a-bbd2-4723-93ce-218ad02d8a31.mov


<!-- ## Table of contents
* [Contact](#contact)
* [Acknowledgments](#acknowledgments) -->


## Installation
Install the package from [PyPi](https://pypi.org/project/typing-filter/) via pip
 ```sh
 pip install typing-filter
 ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Usage
With a list of options ready, a list of descriptions, just import the package call the launch function.
```python
import typing_filter
options = ['Alaska', 'Massachusetts', 'California']
descriptions = [None, 'My home state', 'My current state']
choice = typing_filter.launch(options, descriptions)
```
The selected choice is returned by the launch function, and is None if the operation was canceled.

Additional options can be made by tweaking the launch command:
```python
import typing_filter
options = ['Alaska', 'Massachusetts', 'California']
descriptions = [None, 'My home state', 'My current state']
choice = typing_filter.launch(
  options, descriptions,
  description_separator=': ',
  header='Press Escape to quit!',
  prompt='Input:',
  selector='==>>', selector_padding=3
)
```

<!-- _For more examples, please refer to the [Documentation]._ -->

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Roadmap

Refer to the [Notion Roadmap] for future features and the state of the project.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Contact
Created by [Jonathan Delgado](https://jdelgado.net/).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

[Notion Roadmap]: https://otanan.notion.site/
[Documentation]: https://stochastic-thermodynamics-in-python.readthedocs.io/en/latest/
