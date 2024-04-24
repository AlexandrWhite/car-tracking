from numpy import ndarray
from supervision import LineZoneAnnotator
from supervision.detection.line_zone import LineZone
from supervision.geometry.core import Vector
from supervision.detection.core import Detections

class IdLineAnnotator(LineZoneAnnotator):
    
    def annotate(self, frame: ndarray, line_counter: LineZone, id: int) -> ndarray:
        self.display_in_count = False
        self.display_out_count = False 
        
        text_anchor = Vector(
            start=line_counter.vector.start, end=line_counter.vector.end
        )

        self._annotate_count(frame=frame,
                            center_text_anchor=text_anchor.center,
                            text=f"ID: {id}",
                            is_in_count=True)
        return super().annotate(frame, line_counter)
    