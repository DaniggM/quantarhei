#
#
#  TwoDSpectrumConteiner class functionality
#
#

Feature: TwoDSpectrumContainer should store TwoDSpectra index by various methods
    TwoDSpectrum container should be able to index its content by integer values,
    by arbitrary ValueAxis (including TimeAxis) and by a list of strings 
    (like a dictionary).
    
    
    Scenario Outline: TwoDSpectrumContainer indexes by an integer number
        Given that I have <N> TwoDSpectrum objects
        And I have an empty TwoDSpectrum container
        When I set the container to accept indexing by integers
        And I add the spectra to the container one by one
        Then TwoDSpectrum can be retrieved using the index <i>
        But when index is out of bounds, I get an exception
        
    Examples:
    | N  |  i  |
    | 1  |  0  |
    | 20 |  8  |
    | 12 |  12 |
    | 9  |  3  |


    Scenario Outline: TwoDSpectrumContainer indexes by ValueAxis
        Given that I have <N> TwoDSpectrum objects
        And I have an empty TwoDSpectrum container
        And I have a ValueAxis of lenght <N> starting from zero with certain <step>
        When I set the container to accept index by ValueAxis
        And I add the spectra to the container using values from ValueAxis
        Then TwoDSpectrum can be retrieved using values <val> from ValueAxis
        But when values are out of bounds, I get an exception
        And TwoDSpectrum can be retrieved using the index <i>
        But when index is out of bounds, I get an exception
        
    Examples:
    |  N  |  step  |  val   |  i   |
    |  5  |   0.3  |  0.9   |  4   |
    | 12  |   1.0  |  10.0  |  4   |
    | 12  |   1.0  |  15.0  |  5   |
    | 15  |   2.0  |  16.0  |  10  |
    | 15  |   2.0  |  18.0  |  20  |
    
    
    Scenario Outline: TwoDSpectrumContainer indexes by TimeAxis
        Given that I have <N> TwoDSpectrum objects
        And I have an empty TwoDSpectrum container
        And I have a TimeAxis of lenght <N> starting from zero with certain <step>
        When I set the container to accept index by TimeAxis
        And I add the spectra to the container using values from TimeAxis
        Then TwoDSpectrum can be retrieved using values <val> from TimeAxis
        But when values are out of bounds, I get an exception
        And TwoDSpectrum can be retrieved using the index <i>
        But when index is out of bounds, I get an exception        
        
    Examples:
    |  N  |  step  |  val   |  i   |
    |  5  |   0.3  |  0.9   |  4   |
    | 12  |   1.0  |  10.0  |  4   |
    | 12  |   1.0  |  15.0  |  5   |
    | 15  |   2.0  |  16.0  |  10  |
    | 15  |   2.0  |  18.0  |  20  |


    Scenario Outline: TwoDSpectrumContainer indexes by FrequencyAxis
        Given that I have <N> TwoDSpectrum objects
        And I have an empty TwoDSpectrum container
        And I have a FrequencyAxis of lenght <N> starting from zero with certain <step>
        When I set the container to accept index by FrequencyAxis
        And I add the spectra to the container using values from FrequencyAxis
        Then TwoDSpectrum can be retrieved using values <val> from FrequencyAxis
        But when values are out of bounds, I get an exception
        And TwoDSpectrum can be retrieved using the index <i>
        But when index is out of bounds, I get an exception        
        
    Examples:
    |  N  |  step  |  val   |  i   |
    |  5  |   0.3  |  0.9   |  4   |
    | 12  |   1.0  |  10.0  |  4   |
    | 12  |   1.0  |  15.0  |  5   |
    | 15  |   2.0  |  16.0  |  10  |
    | 15  |   2.0  |  18.0  |  20  |
    

    Scenario Outline: TwoDSpectrumContainer indexes by strings
        Given that I have <N> TwoDSpectrum objects
        And I have an empty TwoDSpectrum container
        And I have a list of strings of lenght <N>
        When I set the container to accept index by strings
        And I add the spectra to the container using values from the list of strings
        Then TwoDSpectrum can be retrieved using values from the list of strings
        But when values are not in the list of strings, I get an exception
        And TwoDSpectrum can be retrieved using the index <i>
        But when index is out of bounds, I get an exception        
        
    Examples:
    |  N  |  i   |
    |  5  |  4   |
    | 12  |  4   |
    | 12  |  5   |
    | 15  |  10  |
    | 15  |  20  |

    